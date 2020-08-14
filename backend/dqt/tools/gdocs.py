from __future__ import print_function
import pickle
import os
import re
import copy
import shutil
import shortuuid
import tempfile

from django.db import connections
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from zipfile import ZipFile
from lxml import etree
from dqt.tools import graphs


class Gdocs:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/documents']

    """Init (authentication etc.) of all necessary services,"""
    def __init__(self, main_template_id):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
                self.create_or_refresh_token()
                self.service = build('docs', 'v1', credentials=self.creds)
                self.drive_service = build('drive', 'v3', credentials=self.creds)
        else:
            raise RuntimeError("Unable to find token file")

        self.create_tempdir()
        
        self.main_template_id = main_template_id
        self.template_ids = set(self.main_template_id)
        self.main_template_id = main_template_id
        self.download(self.main_template_id)
        self.copy_zip(self.main_template_id, self.main_template_id + "_out")

    def create_tempdir(self):
        self.dirpath = tempfile.mkdtemp()

    def destroy_tempdir(self):
        shutil.rmtree(self.dirpath)

    def add_image_file(self, buffer, name='image.png'):
        path = os.path.join(self.dirpath, self.main_template_id + '_out')
        with ZipFile(path, mode='a') as zip_file:
            image_file_path = os.path.join('Pictures/', shortuuid.uuid() + '_' + name)
            zip_file.writestr(image_file_path, buffer.getbuffer())
    
        # Updating manifest
        with ZipFile(path) as zip_file:
            with zip_file.open('META-INF/manifest.xml') as content:
                root = etree.parse(content).getroot()

        self.remove_file_from_zip(path, 'META-INF/manifest.xml')

        namespace = '{urn:oasis:names:tc:opendocument:xmlns:manifest:1.0}'
        root.append(etree.Element(
            namespace + 'file-entry',
            attrib={
                (namespace + 'full-path'): image_file_path,
                (namespace + 'media-type'): 'image/png'
            }
        ))

        with ZipFile(path, mode='a') as zip_file:
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

    """Downloads document with source_id to dirpath location"""
    def download(self, source_id):
        drive_response = self.drive_service.files().export(
            fileId=source_id,
            mimeType="application/vnd.oasis.opendocument.text"
        ).execute()

        with open(os.path.join(self.dirpath, source_id), 'wb') as f:
            f.write(drive_response)

        return drive_response

    """Uploads document"""
    def upload(self, folder_id, template_id, file_name, content):
        path = os.path.join(self.dirpath, template_id + '_out')
        with ZipFile(path, mode="a") as out_zip:
            out_zip.writestr('content.xml', etree.tostring(content))

        file_metadata = {
            'name': file_name,
            'mimeType': 'application/vnd.google-apps.document',
            "parents": [folder_id]
        }

        media = MediaFileUpload(
            path,
            mimetype='application/vnd.oasis.opendocument.text',
            resumable=True
        )

        file = self.drive_service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()

        return file.get('id')

    """Copies zipfile in dirpath location"""
    def copy_zip(self, source_name, target_name):
        with ZipFile(os.path.join(self.dirpath, source_name), 'r') as zipread:
            with ZipFile(os.path.join(self.dirpath, target_name), 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in ("content.xml"):
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)

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
        if template_id not in self.template_ids:
            self.download(template_id)
            self.template_ids.add(template_id)

        with ZipFile(os.path.join(self.dirpath, template_id)) as myzip:
            with myzip.open('content.xml') as content:
                return etree.parse(content).getroot()
