from __future__ import print_function
import pickle
import os.path
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from gdocs.utils import init
from gdocs.utils import copy
from gdocs.utils import get_tags
from gdocs.utils import get_content
from gdocs.utils import update

# The ID of a sample document.
TEMPLATE_DOCUMENT_ID = '1qSWgaomfyd6serjz70dGHlGG7TsMQyUTkd84o4nSAVk'

COPY_ID = "1l7YriELY6Jb2ziBE1txRVnuUr7EzuUgjsVFFPOorNLg"

SUBTEMPLATE_ID = "1PQzxjC-BEYF4MdgOu0uZFc6cVq3ZKf_4B_pXDduzH3Q"


def main():
    init()

    # report_id = copy(TEMPLATE_DOCUMENT_ID, "Copy test")
    # print(report_id)
    content = get_content(SUBTEMPLATE_ID)

    requests = []
    for node in content:
        if 'paragraph' in node:
            elements = node.get('paragraph').get('elements')

            for element in elements:
                text_run = element.get('textRun')
                if not text_run:
                    continue
                insert = {
                    "insertText": {
                        "location": {
                            "index": 15
                        },
                        "text": text_run.get('content')
                    }
                }

                requests.append(insert)

    print(update(TEMPLATE_DOCUMENT_ID, requests))

    # print(json.dumps(content, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
