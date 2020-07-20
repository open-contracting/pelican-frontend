from __future__ import print_function
import pickle
import os.path
import json

import lxml.etree as etree
from zipfile import ZipFile
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from gdocs.utils import init
from gdocs.utils import get_tags
from gdocs.utils import download
from gdocs.utils import upload
from gdocs.utils import copy_zip
from gdocs.utils import get_template
from gdocs.utils import get_main_template
from gdocs.utils import merge_templates
from gdocs.utils import get_tags


from odf.opendocument import load

# The ID of a sample document.
TEMPLATE_DOCUMENT_ID = '1kES07KZRc7VcEfh0cCWZvHpwIidCMlgvD0XRECoO-lY'

SUBTEMPLATE_ID = "1PQzxjC-BEYF4MdgOu0uZFc6cVq3ZKf_4B_pXDduzH3Q"

FOLDER_ID = "1yLTCRV3yoBM5Goc93SaO4irxnd0iapnK"


def main():
    init()

    main_template = get_main_template(TEMPLATE_DOCUMENT_ID)

    main_template = process_template(main_template, None)

    print(etree.tostring(main_template))

    upload(FOLDER_ID, TEMPLATE_DOCUMENT_ID, "test_upload_4", main_template)
    print("ok")


def process_template(template, parent_tag):
    tags = get_tags(template)
    for tag in tags:
        if tag["name"] == "template":
            template_id = ""
            for param in tag["params"]:
                if param["name"] == "id":
                    template_id = param["value"]

            if not template_id:
                raise ValueError("Missing template id in {}".format(tag["full"]))

            sub_template = get_template(template_id)

            sub_template = process_template(sub_template, tag)

            template = merge_templates(template, sub_template, tag["full"])

    return template


if __name__ == '__main__':
    main()
