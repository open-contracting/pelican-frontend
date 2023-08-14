from datetime import datetime

import simplejson as json
from django.conf import settings
from django.http import JsonResponse
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt

from exporter.exceptions import GoogleDriveError, TagError
from exporter.gdocs import Gdocs
from exporter.template_tags.base import base as base_tag


@csrf_exempt
def generate_report(request) -> JsonResponse:
    if request.method == "GET":
        return JsonResponse({"status": "report_error", "data": {"reason": "Only POST method is accepted."}})

    input_message = json.loads(request.body)

    # checking input_message correctness
    if (
        "dataset_id" not in input_message
        or not isinstance(input_message["dataset_id"], int)
        or "document_id" not in input_message
        or "folder_id" not in input_message
    ):
        return JsonResponse(
            {"status": "report_error", "data": {"reason": "Input message is malformed, will be dropped."}}
        )

    if "language" in input_message and input_message["language"] in dict(settings.LANGUAGES):
        translation.activate(input_message["language"])
    else:
        translation.activate("en")

    document_id = input_message["document_id"].strip()
    folder_id = input_message["folder_id"].strip()

    gdocs = None

    failed_tags = []
    try:
        gdocs = Gdocs(document_id)
        base = base_tag(gdocs, input_message["dataset_id"])
        base.set_argument("template", document_id)
        base.finalize_arguments()
        content, failed_tags = base.validate_and_render({})

        if "report_name" in input_message and isinstance(input_message["report_name"], str):
            filename = input_message["report_name"]
        else:
            filename = f"Report {input_message['dataset_id']} {datetime.now()}"

        file_id = gdocs.upload(folder_id, filename, content)

        response = JsonResponse({"status": "ok", "data": {"file_id": file_id}, "failed_tags": failed_tags})
    except GoogleDriveError as er:
        response = JsonResponse({"status": "report_error", "data": {"reason": str(er)}})
    except TagError as er:
        response = JsonResponse(
            {
                "status": "template_error",
                "data": [er.as_dict()],  # Can accommodate multiple TagErrors in the future
                "failed_tags": failed_tags,
            }
        )
    finally:
        if gdocs is not None:
            gdocs.destroy_tempdir()

    # restores default english translations
    translation.activate("en")
    return response
