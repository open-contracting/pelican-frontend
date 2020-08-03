from __future__ import print_function
import pickle
import os
import re
import shutil
import lxml.etree as etree
import shortuuid
import tempfile

from django.db import connections
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from zipfile import ZipFile


class Gdocs:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/documents']

    creds = None
    service = None
    drive_service = None
    dirpath = None
    template_ids = set()

    """Init (authentication etc.) of all necessary services,"""
    def __init__(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
                self.create_or_refresh_token()
                self.service = build('docs', 'v1', credentials=self.creds)
                self.drive_service = build('drive', 'v3', credentials=self.creds)
        else:
            raise RuntimeError("Unable to find token file")

        self.create_tempdir()

    def create_tempdir(self):
        self.dirpath = tempfile.mkdtemp()

    def destroy_tempdir(self):
        shutil.rmtree(self.dirpath)

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

    def get_main_template(self, template_id):
        self.download(template_id)
        self.copy_zip(template_id, template_id + "_out")
        self.template_ids.add(template_id)

        with ZipFile(os.path.join(self.dirpath, template_id)) as myzip:
            with myzip.open('content.xml') as content:
                return etree.parse(content).getroot()

    def get_template(self, template_id):
        if template_id not in self.template_ids:
            self.download(template_id)
            self.template_ids.add(template_id)

        with ZipFile(os.path.join(self.dirpath, template_id)) as myzip:
            with myzip.open('content.xml') as content:
                return etree.parse(content).getroot()


def get_template_content(template):
    for node in template.xpath(
        '//office:text',
        namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
    ):
        return node


def get_template_styles(template):
    for node in template.xpath(
        '//office:automatic-styles',
        namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
    ):
        return node


DEFAULT_STYLES = (
    "Standard",
    "Heading",
    "Text_20_body",
    "List",
    "Caption",
    "Index",
    "normal",
    "Heading_20_1",
    "Heading_20_2",
    "Heading_20_3",
    "Heading_20_4",
    "Heading_20_5",
    "Heading_20_6",
    "Title",
    "Subtitle",
    "Header",
    "Graphics",
)
def merge_templates(main_template, sub_template, location):
    prefix = shortuuid.uuid()
    sub_template_content = get_template_content(sub_template)
    for location_node in main_template.xpath('.//*[contains(text(),"' + location + '")]'):
        parent = location_node.getparent()

        previous = location_node
        for child in sub_template_content:
            if not "sequence-decls" in child.tag:
                # lets rename all paragraph styles to standard
                for attrib in child.attrib:
                    if "style-name" in attrib and child.get(attrib) == "P1":
                        child.set(attrib, "Standard")

                for node in child:
                    for attrib in node.attrib:
                        if attrib.endswith("style-name"):
                            if node.get(attrib) not in DEFAULT_STYLES:
                                node.set(attrib, prefix + node.get(attrib))

                previous.addnext(child)
                previous = child

        # remove the template node
        parent.remove(location_node)

    main_template = merge_template_styles(main_template, sub_template, prefix)
    return main_template


def merge_template_styles(main_template, sub_template, prefix):
    sub_template_styles = get_template_styles(sub_template)

    for main_style_node in main_template.xpath(
        '//office:automatic-styles',
        namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
    ):
        for sub_style in sub_template_styles:
            # lets rename all paragraph styles to standard
            for attrib in sub_style.attrib:
                if attrib.endswith("name"):
                    sub_style.set(attrib, prefix + sub_style.get(attrib))

            main_style_node.append(sub_style)

    return main_template


def set_tag_value(main_template, value, location):
    for node in main_template.xpath('.//*[contains(text(),"' + location + '")]'):
        if node.text and location in node.text:
            node.text = node.text.replace(location, str(value))
        else:
            for subnode in node:
                if location in subnode.tail:
                    subnode.tail = subnode.tail.replace(location, str(value))

    return main_template


def get_tags(template):
    tags = []

    for node in template.xpath('.//text()'):

        lines = re.findall("{%.*%}", node)

        for line in lines:
            tag = {}
            tag["full"] = line

            line = line[2:-2]

            chunks = line.split()
            tag["name"] = chunks[0]

            params = []
            if len(chunks) > 1:
                for chunk in chunks[1:]:
                    parts = chunk.split(':|')
                    param = {}
                    param["name"] = parts[0]
                    if len(parts) > 1:
                        param["value"] = parts[1][:-1]

                    params.append(param)
            tag["params"] = params
            tags.append(tag)

    return tags


def get_template_id(tag):
    template_id = None
    for param in tag["params"]:
        if param["name"] == "id":
            template_id = param["value"]

    return template_id


def get_tag_param(tag, param_name):
    param_value = [param['value'] for param in tag['params'] if param['name'] == param_name]
    if param_value:
        return param_value[0]
    else:
        return None


ELEMENTAL_TAGS = (
    "checkedCount",
    "passedCount",
    "failedCount",
    "notAvailableCount",
    "name",
    "description",
    "passedExamples",
    "failedExamples",
    "undefinedExamples",
    "coverageCheckedCount",
    "coveragePassedCount",
    "coverageFailedCount",
    "qualityCheckedCount",
    "qualityPassedCount",
    "qualityFailedCount",
    "coveragePassedExamples",
    "coverageFailedExamples",
    "qualityPassedExamples",
    "qualityFailedExamples",
)
def process_template(template, data, gdocs, dataset_id):
    tags = get_tags(template)

    for tag in tags:
        if tag["name"] == "summary":
            template = set_tag_value(template, "This is a very long summary", tag["full"])

        if tag["name"] == "field":
            template_id = get_tag_param(tag, 'template')

            if not template_id:
                template_id = "1Is3yi1p3XRI1x98rTZcfQiKb7WAAC4P1nXb-VCCyVTk"

            sub_template = gdocs.get_template(template_id)
            check_name = get_tag_param(tag, 'check')
            # TODO: the param check is necessary

            with connections["data"].cursor() as cursor:
                cursor.execute(
                    """
                    select data->%s
                    from report
                    where dataset_id = %s and
                        type = 'field_level_check' and
                        data ? %s;
                    """, [check_name, dataset_id, check_name]
                )
                rows = cursor.fetchall()

                if not rows:
                    continue

                result = rows[0][0]

                # getting examples
                cursor.execute(
                    """
                    select data
                    from field_level_check_examples
                    where dataset_id = %s and path = %s;
                    """, [dataset_id, check_name]
                )
                result_examples = cursor.fetchall()[0][0]

                result['coverage']['passed_examples'] = result_examples['coverage']['passed_examples']
                result['coverage']['failed_examples'] = result_examples['coverage']['failed_examples']
                result['quality']['passed_examples'] = result_examples['quality']['passed_examples']
                result['quality']['failed_examples'] = result_examples['quality']['failed_examples']

                data = {
                    "coverageCheckedCount": result['coverage']['total_count'],
                    "coveragePassedCount": result['coverage']['passed_count'],
                    "coverageFailedCount": result['coverage']['failed_count'],
                    "qualityCheckedCount": result['quality']['total_count'],
                    "qualityPassedCount": result['quality']['passed_count'],
                    "qualityFailedCount": result['quality']['failed_count'],
                    
                    "name": check_name, # TODO: temporary
                    "description": "placeholder", # TODO: placeholder
                    "coveragePassedExamples": ', '.join(example['meta']['ocid'] for example in result['coverage']['passed_examples']),
                    "coverageFailedExamples": ', '.join(example['meta']['ocid'] for example in result['coverage']['failed_examples']),
                    "qualityPassedExamples": ', '.join(example['meta']['ocid'] for example in result['quality']['passed_examples']),
                    "qualityFailedExamples": ', '.join(example['meta']['ocid'] for example in result['quality']['failed_examples']),
                }

            sub_template = process_template(sub_template, data, gdocs, dataset_id)
            template = merge_templates(template, sub_template, tag["full"])


        if tag["name"] == "resource":
            template_id = get_tag_param(tag, 'template')

            if not template_id:
                template_id = "1ZgKP1TWU8AbnOFhjEqlBO--lR71dAlNMyiGDUh8MZ-8"

            sub_template = gdocs.get_template(template_id)
            check_name = get_tag_param(tag, 'check')
            # TODO: the param check is necessary

            with connections["data"].cursor() as cursor:
                cursor.execute(
                    """
                    select data->%s
                    from report
                    where dataset_id = %s and
                        type = 'resource_level_check' and
                        data ? %s;
                    """, [check_name, dataset_id, check_name]
                )
                rows = cursor.fetchall()

                if not rows:
                    continue

                result_report = rows[0][0]

                # getting examples
                cursor.execute(
                    """
                    select data
                    from resource_level_check_examples
                    where dataset_id = %s and
                        check_name = %s;
                    """, [dataset_id, check_name]
                )
                result_examples = cursor.fetchall()[0][0]
                result = {**result_report, **result_examples}

                # TODO: no rows retrieved
                data = {
                    "checkedCount": result['total_count'],
                    "passedCount": result['passed_count'],
                    "failedCount": result['failed_count'],
                    "notAvailableCount": result['undefined_count'],
                    "name": check_name, # TODO: temporary
                    "description": "placeholder", # TODO: placeholder
                    "passedExamples": ', '.join(example['meta']['ocid'] for example in result['passed_examples']),
                    "failedExamples": ', '.join(example['meta']['ocid'] for example in result['failed_examples']),
                    "undefinedExamples": ', '.join(example['meta']['ocid'] for example in result['undefined_examples']),
                }

            sub_template = process_template(sub_template, data, gdocs, dataset_id)
            template = merge_templates(template, sub_template, tag["full"])

        # elemental tags
        if tag["name"] in ELEMENTAL_TAGS:
            template = set_tag_value(template, data[tag["name"]], tag["full"])

    return template