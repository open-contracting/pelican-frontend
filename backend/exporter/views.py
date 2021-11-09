from datetime import datetime

import simplejson as json
from django.conf import settings
from django.http import JsonResponse
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt

from .exceptions import GoogleDriveError, TagError
from .gdocs import Gdocs
from .tags.template_tags.base import BaseTemplateTag


@csrf_exempt
def generate_report(request):
    if request.method == "GET":
        return JsonResponse({"status": "report_error", "data": {"reason": "Only post method is accepted."}})

    body_unicode = request.body.decode("utf-8")
    input_message = json.loads(body_unicode)

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
        # switch to input language
        translation.activate(input_message["language"])
    else:
        translation.activate("en")

    response = None
    gdocs = None

    try:
        gdocs = Gdocs(input_message["document_id"])
        base = BaseTemplateTag(gdocs, input_message["dataset_id"])
        base.set_param("template", input_message["document_id"])
        base.finalize_params()
        failed_tags = []
        main_template, failed_tags = base.validate_and_process({})

        report_name = "Report %s %s" % (input_message["dataset_id"], datetime.now())
        if "report_name" in input_message and isinstance(input_message["report_name"], str):
            report_name = input_message["report_name"]

        file_id = gdocs.upload(input_message["folder_id"], report_name, main_template)

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
