from __future__ import print_function
import pickle
import os
import re
import copy
import json
import shutil
import datetime
import shortuuid
import tempfile

from django.db import connections
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.api_core.datetime_helpers import from_rfc3339
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import ResumableUploadError, HttpError
from zipfile import ZipFile
from lxml import etree
from dqt.tools import graphs
from dqt.tools.errors import GoogleDriveError


class Gdocs:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/documents']
    OUT_FILE_NAME = 'out'

    """Init (authentication etc.) of all necessary services,"""
    def __init__(self, main_template_id):
        # TODO: use default_storage
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
                self.create_or_refresh_token()
                self.service = build('docs', 'v1', credentials=self.creds)
                self.drive_service = build('drive', 'v3', credentials=self.creds)
        else:
            raise RuntimeError("Unable to find token file")

        self.dirpath = self.create_tempdir()
        self.google_drive_cache = GoogleDriveCache(self.drive_service)
        
        self.main_template_id = main_template_id
        self.main_template_path = os.path.join(self.dirpath, Gdocs.OUT_FILE_NAME)
        cache_file_path = self.google_drive_cache.get_file_path(main_template_id)
        with ZipFile(cache_file_path, 'r') as zipread:
            with ZipFile(self.main_template_path, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in ("content.xml"):
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)

    def create_tempdir(self):
        return tempfile.mkdtemp()

    def destroy_tempdir(self):
        shutil.rmtree(self.dirpath)

    def add_image_file(self, buffer, name='image.png'):
        with ZipFile(self.main_template_path, mode='a') as zip_file:
            image_file_path = os.path.join('Pictures/', shortuuid.uuid() + '_' + name)
            zip_file.writestr(image_file_path, buffer.getbuffer())

        # Updating manifest
        with ZipFile(self.main_template_path) as zip_file:
            with zip_file.open('META-INF/manifest.xml') as content:
                root = etree.parse(content).getroot()

        self.remove_file_from_zip(self.main_template_path, 'META-INF/manifest.xml')

        namespace = '{urn:oasis:names:tc:opendocument:xmlns:manifest:1.0}'
        root.append(etree.Element(
            namespace + 'file-entry',
            attrib={
                (namespace + 'full-path'): image_file_path,
                (namespace + 'media-type'): 'image/png'
            }
        ))

        with ZipFile(self.main_template_path, mode='a') as zip_file:
            zip_file.writestr('META-INF/manifest.xml', etree.tostring(root))

        return image_file_path

    """Creates or refresh of auth token"""
    def create_or_refresh_token(self):
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json",
                    "https: // www.googleapis.com/auth/documents"
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            # TODO: resolve race condition
            # with open('token.pickle', 'wb') as token:
            #     pickle.dump(self.creds, token)

    """Uploads document"""
    def upload(self, folder_id, file_name, content):
        with ZipFile(self.main_template_path, mode="a") as out_zip:
            out_zip.writestr('content.xml', etree.tostring(content))

        file_metadata = {
            'name': file_name,
            'mimeType': 'application/vnd.google-apps.document',
            "parents": [folder_id]
        }

        media = MediaFileUpload(
            self.main_template_path,
            mimetype='application/vnd.oasis.opendocument.text',
            resumable=True
        )

        try:
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media
            ).execute()
        except ResumableUploadError as er:
            self.destroy_tempdir()
            raise GoogleDriveError(
                'The final report could not be uploaded to folder with id \'%s\'. Please review the permission settings.' % folder_id
            )

        return file.get('id')

    def remove_file_from_zip(self, zip_file_path, file_path):
        with ZipFile(zip_file_path, 'r') as zipread:
            with ZipFile(zip_file_path + '_copy', 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename != file_path:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)

        shutil.move(zip_file_path + '_copy', zip_file_path)

    def get_main_template(self):
        return self.get_template(self.main_template_id)

    def get_template(self, template_id):
        cache_file_path = self.google_drive_cache.get_file_path(template_id)
        with ZipFile(cache_file_path) as myzip:
            with myzip.open('content.xml') as content:
                return etree.parse(content).getroot()


class GoogleDriveCache:
    ROOT = 'google_drive_cache'

    def __init__(self, drive_service):
        if not default_storage.exists(GoogleDriveCache.ROOT):
            os.mkdir(os.path.join(default_storage.location, GoogleDriveCache.ROOT))
        
        self.drive_service = drive_service
        self.files = dict()
        self.refresh()

    def refresh(self):
        self.files = dict()
        _, filenames = default_storage.listdir(GoogleDriveCache.ROOT)
        # print(filenames)
        for filename in filenames:
            rfc3339, file_id = re.search(r'^([^_]+)_(.+)$', filename).groups()
            last_modified = from_rfc3339(rfc3339)
            if (file_id in self.files and last_modified > self.files[file_id]['last_modified']) or \
                    (file_id not in self.files):
                self.files[file_id] = {
                    'last_modified': last_modified,
                    'path': os.path.join(GoogleDriveCache.ROOT, filename)
                }

    def get_file_path(self, file_id):
        self.refresh()

        drive_response = self.drive_service.files().get(
            fileId=file_id,
            fields='modifiedTime'
        ).execute()
        last_modified_rfc3339 = drive_response['modifiedTime']
        last_modified = from_rfc3339(drive_response['modifiedTime'])
        print('NEW: %s, OLD: %s' % (last_modified, self.files[file_id]['last_modified']))
        if (file_id in self.files and last_modified > self.files[file_id]['last_modified']) or \
                (file_id not in self.files):
            try:
                drive_response = self.drive_service.files().export(
                    fileId=file_id,
                    mimeType="application/vnd.oasis.opendocument.text"
                ).execute()
            except HttpError as er:
                raise GoogleDriveError(
                    'File with id \'%s\' could not be downloaded. Please review the permission settings.' % source_id
                )

            return default_storage.save(
                os.path.join(GoogleDriveCache.ROOT, last_modified_rfc3339 + '_' + file_id),
                ContentFile(drive_response)
            )

        return self.files[file_id]['path']





