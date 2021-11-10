import json
import os
import re
import shutil
import tempfile
from zipfile import ZipFile

import shortuuid
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, ResumableUploadError
from googleapiclient.http import MediaFileUpload
from lxml import etree

from exporter.exceptions import GoogleDriveError


class Gdocs:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/documents"]
    OUT_FILE_NAME = "out"

    """Init (authentication etc.) of all necessary services,"""

    def __init__(self, main_template_id):
        # TODO: use default_storage
        if os.path.exists(settings.TOKEN_PATH):
            with open(settings.TOKEN_PATH) as f:
                self.creds = Credentials.from_authorized_user_info(json.load(f))
                self.drive_service = build("drive", "v3", credentials=self.creds)
        else:
            raise RuntimeError("Unable to find token file")

        self.dirpath = self.create_tempdir()
        self.google_drive_cache = GoogleDriveCache(self.drive_service)

        self.main_template_id = main_template_id
        self.main_template_path = os.path.join(self.dirpath, Gdocs.OUT_FILE_NAME)
        cache_file_path = self.google_drive_cache.get_file_path(main_template_id)
        with ZipFile(cache_file_path, "r") as zipread:
            with ZipFile(self.main_template_path, "w") as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in ("content.xml"):
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)

    def create_tempdir(self):
        return tempfile.mkdtemp()

    def destroy_tempdir(self):
        shutil.rmtree(self.dirpath)

    def add_image_file(self, buffer, name="image.png"):
        with ZipFile(self.main_template_path, mode="a") as zip_file:
            image_file_path = os.path.join("Pictures/", shortuuid.uuid() + "_" + name)
            zip_file.writestr(image_file_path, buffer.getbuffer())

        # Updating manifest
        with ZipFile(self.main_template_path) as zip_file:
            with zip_file.open("META-INF/manifest.xml") as content:
                root = etree.parse(content).getroot()

        self.remove_file_from_zip(self.main_template_path, "META-INF/manifest.xml")

        namespace = "{urn:oasis:names:tc:opendocument:xmlns:manifest:1.0}"
        root.append(
            etree.Element(
                namespace + "file-entry",
                attrib={(namespace + "full-path"): image_file_path, (namespace + "media-type"): "image/png"},
            )
        )

        with ZipFile(self.main_template_path, mode="a") as zip_file:
            zip_file.writestr("META-INF/manifest.xml", etree.tostring(root))

        return image_file_path

    """Uploads document"""

    def upload(self, folder_id, file_name, content):
        with ZipFile(self.main_template_path, mode="a") as out_zip:
            out_zip.writestr("content.xml", etree.tostring(content))

        file_metadata = {"name": file_name, "mimeType": "application/vnd.google-apps.document", "parents": [folder_id]}

        media = MediaFileUpload(
            self.main_template_path, mimetype="application/vnd.oasis.opendocument.text", resumable=True
        )

        try:
            file = self.drive_service.files().create(body=file_metadata, media_body=media).execute()
        except ResumableUploadError:
            raise GoogleDriveError(
                f"The final report could not be uploaded to folder with id '{folder_id}'. "
                "Possible reasons are a non-existing folder or insufficient permission settings."
            )

        return file.get("id")

    def remove_file_from_zip(self, zip_file_path, file_path):
        with ZipFile(zip_file_path, "r") as zipread:
            with ZipFile(zip_file_path + "_copy", "w") as zipwrite:
                for item in zipread.infolist():
                    if item.filename != file_path:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)

        shutil.move(zip_file_path + "_copy", zip_file_path)

    def get_main_template(self):
        return self.get_template(self.main_template_id)

    def get_template(self, template_id):
        cache_file_path = self.google_drive_cache.get_file_path(template_id)
        with ZipFile(cache_file_path) as myzip:
            with myzip.open("content.xml") as content:
                return etree.parse(content).getroot()


class GoogleDriveCache:
    ROOT = "google_drive_cache"
    NO_OF_ATTEMPTS = 5

    def __init__(self, drive_service):
        if not default_storage.exists(GoogleDriveCache.ROOT):
            os.mkdir(os.path.join(default_storage.location, GoogleDriveCache.ROOT))

        self.drive_service = drive_service
        self.files = dict()
        self.refresh()

    def refresh(self):
        self.files = dict()
        _, filenames = default_storage.listdir(GoogleDriveCache.ROOT)
        for filename in filenames:
            version, file_id = re.search(r"^([^_]+)_(.+)$", filename).groups()
            version = int(version)
            if (file_id in self.files and version > self.files[file_id]["version"]) or (file_id not in self.files):
                self.files[file_id] = {"version": version, "path": os.path.join(GoogleDriveCache.ROOT, filename)}

    def get_file_path(self, file_id):
        self.refresh()

        drive_response = None
        for i in range(GoogleDriveCache.NO_OF_ATTEMPTS):
            try:
                drive_response = self.drive_service.files().get(fileId=file_id, fields="version").execute()

                break
            except HttpError:
                if i > (GoogleDriveCache.NO_OF_ATTEMPTS - 2):
                    raise GoogleDriveError(
                        f"File with id '{file_id}' could not be accessed. "
                        "Possible reasons are a non-existing file or insufficient permission settings."
                    )

        version = int(drive_response["version"])

        if (file_id in self.files and version > self.files[file_id]["version"]) or (file_id not in self.files):

            drive_response = None
            for i in range(GoogleDriveCache.NO_OF_ATTEMPTS):
                try:
                    drive_response = (
                        self.drive_service.files()
                        .export(fileId=file_id, mimeType="application/vnd.oasis.opendocument.text")
                        .execute()
                    )

                    break
                except HttpError:
                    if i > (GoogleDriveCache.NO_OF_ATTEMPTS - 2):
                        raise GoogleDriveError(
                            f"File with id '{file_id}' could not be downloaded. "
                            "Possible reasons are a non-existing folder or insufficient permission settings."
                        )

            return default_storage.save(
                os.path.join(GoogleDriveCache.ROOT, str(version) + "_" + file_id), ContentFile(drive_response)
            )
        else:
            return self.files[file_id]["path"]
