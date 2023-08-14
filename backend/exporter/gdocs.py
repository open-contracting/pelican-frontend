# All interactions with Google Drive APIs should be in this file.

import os
import re
import shutil
import tempfile
from zipfile import ZipFile

import shortuuid
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, ResumableUploadError
from googleapiclient.http import MediaFileUpload
from lxml import etree

from exporter.exceptions import GoogleDriveError

ROOT = "google_drive_cache"
NO_OF_ATTEMPTS = 5


class Gdocs:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/documents"]

    """Init (authentication etc.) of all necessary services,"""

    def __init__(self, main_template_id: str):
        # TODO: use default_storage
        if not os.path.exists(settings.SERVICE_ACCOUNT_JSON_FILE):
            raise RuntimeError("Unable to find token file")

        credentials = Credentials.from_service_account_file(settings.SERVICE_ACCOUNT_JSON_FILE)
        self.drive_service = build("drive", "v3", credentials=credentials, cache_discovery=False)
        self.google_drive_cache = GoogleDriveCache(self.drive_service)

        self.directory = tempfile.mkdtemp()
        self.output_file = os.path.join(self.directory, "out.zip")

        with ZipFile(self.google_drive_cache.get_file_path(main_template_id), "r") as zipread:
            with ZipFile(self.output_file, "w") as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in ("content.xml"):
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)

    def destroy_tempdir(self) -> None:
        shutil.rmtree(self.directory)

    def add_image_file(self, buffer, name: str = "image.png") -> str:
        with ZipFile(self.output_file, mode="a") as zipfile:
            path = os.path.join("Pictures/", f"{shortuuid.uuid()}_{name}")
            zipfile.writestr(path, buffer.getbuffer())

        # Updating manifest
        with ZipFile(self.output_file) as zipfile:
            with zipfile.open("META-INF/manifest.xml") as content:
                root = etree.parse(content).getroot()

        self.remove_file_from_zip(self.output_file, "META-INF/manifest.xml")

        namespace = "{urn:oasis:names:tc:opendocument:xmlns:manifest:1.0}"
        root.append(
            etree.Element(
                f"{namespace}file-entry",
                attrib={f"{namespace}full-path": path, f"{namespace}media-type": "image/png"},
            )
        )

        with ZipFile(self.output_file, mode="a") as zipfile:
            zipfile.writestr("META-INF/manifest.xml", etree.tostring(root))

        return path

    def upload(self, folder_id: str, file_name: str, content: etree.Element):
        with ZipFile(self.output_file, mode="a") as zipfile:
            zipfile.writestr("content.xml", etree.tostring(content))

        file_metadata = {"name": file_name, "mimeType": "application/vnd.google-apps.document", "parents": [folder_id]}

        media = MediaFileUpload(self.output_file, mimetype="application/vnd.oasis.opendocument.text", resumable=True)

        try:
            file = self.drive_service.files().create(body=file_metadata, media_body=media).execute()
        except ResumableUploadError:
            raise GoogleDriveError(
                f"The final report could not be uploaded to folder ID '{folder_id}'. "
                "Possible reasons are a non-existing folder or insufficient permission settings."
            )

        return file.get("id")

    def remove_file_from_zip(self, zip_file_path: str, file_path: str) -> None:
        with ZipFile(zip_file_path, "r") as zipread:
            with ZipFile(f"{zip_file_path}_copy", "w") as zipwrite:
                for item in zipread.infolist():
                    if item.filename != file_path:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)

        shutil.move(f"{zip_file_path}_copy", zip_file_path)

    def get_content(self, file_id: str) -> etree.Element:
        with ZipFile(self.google_drive_cache.get_file_path(file_id)) as zipfile:
            with zipfile.open("content.xml") as content:
                return etree.parse(content).getroot()


class GoogleDriveCache:
    def __init__(self, drive_service):
        if not default_storage.exists(ROOT):
            os.mkdir(os.path.join(default_storage.location, ROOT))

        self.drive_service = drive_service
        self.files = {}
        self.refresh()

    def refresh(self) -> None:
        self.files = {}
        _, filenames = default_storage.listdir(ROOT)
        for filename in filenames:
            version, file_id = re.search(r"^([^_]+)_(.+)$", filename).groups()
            version = int(version)
            if (file_id in self.files and version > self.files[file_id]["version"]) or (file_id not in self.files):
                self.files[file_id] = {"version": version, "path": os.path.join(ROOT, filename)}

    def get_file_path(self, file_id: str):
        self.refresh()

        drive_response = None
        for i in range(NO_OF_ATTEMPTS):
            try:
                drive_response = self.drive_service.files().get(fileId=file_id, fields="version").execute()

                break
            except HttpError:
                if i > (NO_OF_ATTEMPTS - 2):
                    raise GoogleDriveError(
                        f"Template ID '{file_id}' could not be accessed. "
                        "Possible reasons are a non-existing file or insufficient permission settings."
                    )

        version = int(drive_response["version"])

        if (file_id in self.files and version > self.files[file_id]["version"]) or (file_id not in self.files):
            drive_response = None
            for i in range(NO_OF_ATTEMPTS):
                try:
                    drive_response = (
                        self.drive_service.files()
                        .export(fileId=file_id, mimeType="application/vnd.oasis.opendocument.text")
                        .execute()
                    )

                    break
                except HttpError:
                    if i > (NO_OF_ATTEMPTS - 2):
                        raise GoogleDriveError(
                            f"Template ID '{file_id}' could not be downloaded. "
                            "Possible reasons are a non-existing file or insufficient permission settings."
                        )

            return default_storage.save(os.path.join(ROOT, f"{version}_{file_id}"), ContentFile(drive_response))
        else:
            return self.files[file_id]["path"]
