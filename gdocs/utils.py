from __future__ import print_function
import pickle
import os.path
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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


def copy(source_id, new_title):
    """Copy document with source_id, set new title and return the id of a new document"""
    body = {
        'name': new_title
    }

    drive_response = drive_service.files().copy(
        fileId=source_id, body=body).execute()
    copy_id = drive_response.get('id')

    return copy_id


def update(doc_id, requests):
    """Performs batch update in a document"""

    result = service.documents().batchUpdate(
        documentId=doc_id, body={'requests': requests}).execute()

    return result


def get_content(document_id):
    """Document content"""
    document = service.documents().get(documentId=document_id).execute()
    return document.get('body').get('content')


def get_plain_text(document_id):
    """Returns plain text from the document"""
    document = service.documents().get(documentId=document_id).execute()
    content = document.get('body').get('content')
    return read_structural_elements(content)


def get_tags(document_id):
    content = get_plain_text(document_id)

    lines = re.findall("{%.*%}", content)
    tags = []

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


def get_tag_start_index(content, search_text):
    """Returns the paragraph elements with text containing search_text.

        Args:
            content: a list of elements from a Google Doc.
            search_text:
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text
