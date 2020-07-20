from __future__ import print_function
import pickle
import os.path
import re
import lxml.etree as etree
import shortuuid

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from zipfile import ZipFile

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

creds = None
service = None
drive_service = None


def init():
    """Init (authentication etc.) of all necessary services,"""
    if os.path.exists('./gdocs/token.pickle'):
        with open('./gdocs/token.pickle', 'rb') as token:
            global creds
            creds = pickle.load(token)

            create_or_refresh_token()

            global service
            service = build('docs', 'v1', credentials=creds)

            global drive_service
            drive_service = build('drive', 'v3', credentials=creds)
    else:
        raise RuntimeError("Unable to find token file")


def create_or_refresh_token():
    """Creates or refresh of auth token"""
    global creds
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./gdocs/credentials.json", "https: // www.googleapis.com/auth/documents")
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./gdocs/token.pickle', 'wb') as token:
            pickle.dump(creds, token)


def download(source_id, path):
    """Downloads document with source_id"""
    drive_response = drive_service.files().export(
        fileId=source_id, mimeType="application/vnd.oasis.opendocument.text").execute()

    f = open(path, "wb")
    f.write(drive_response)
    f.close()

    return drive_response


def upload(folder_id, template_id, file_name, content):
    path = "/tmp/{}_out".format(template_id)
    with ZipFile(path, mode="a") as out_zip:
        out_zip.writestr('content.xml', etree.tostring(content))

    file_metadata = {
        'name': file_name,
        'mimeType': 'application/vnd.google-apps.document',
        "parents": [folder_id]
    }

    media = MediaFileUpload(path,
                            mimetype='application/vnd.oasis.opendocument.text',
                            resumable=True)

    file = drive_service.files().create(body=file_metadata,
                                        media_body=media).execute()

    print("File ID: {}".format(file.get('id')))


def copy_zip(source, target):
    with ZipFile(source, 'r') as zipread:
        with ZipFile(target, 'w') as zipwrite:
            for item in zipread.infolist():
                if item.filename not in ("content.xml"):
                    data = zipread.read(item.filename)
                    zipwrite.writestr(item, data)


def get_main_template(template_id):
    path = "/tmp/{}".format(template_id)
    download(template_id, path)

    copy_zip(path, path + "_out")

    with ZipFile(path) as myzip:
        with myzip.open('content.xml') as content:
            return etree.parse(content).getroot()


def get_template(template_id):
    path = "/tmp/{}".format(template_id)
    download(template_id, path)

    with ZipFile(path) as myzip:
        with myzip.open('content.xml') as content:
            return etree.parse(content).getroot()


def get_template_content(template):
    for node in template.xpath('//office:text',
                               namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}):
        return node


def get_template_styles(template):
    for node in template.xpath('//office:automatic-styles',
                               namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}):
        return node


def merge_templates(main_template, sub_template, location):
    prefix = shortuuid.uuid()
    sub_template_content = get_template_content(sub_template)
    for location_node in main_template.xpath('.//*[contains(text(),"' + location + '")]'):
        parent = location_node.getparent()

        previous = parent
        for child in sub_template_content:
            if not "sequence-decls" in child.tag:
                # lets rename all paragraph styles to standard
                for attrib in child.attrib:
                    if "style-name" in attrib:
                        child.set(attrib, "Standard")

                for node in child:
                    for attrib in node.attrib:
                        if attrib.endswith("style-name"):
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
            '//office:automatic-styles', namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}):

        for sub_style in sub_template_styles:
            # lets rename all paragraph styles to standard
            for attrib in sub_style.attrib:
                if attrib.endswith("name"):
                    sub_style.set(attrib, prefix + sub_style.get(attrib))

            main_style_node.append(sub_style)

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
