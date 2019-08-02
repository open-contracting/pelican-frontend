from django.db.models import Count, Sum
from django.http import JsonResponse

from .models import ResourceLevelCheck


def resource_level_stats(request, dataset_id):

    result = {}

    counts = ResourceLevelCheck.objects.filter(dataset=dataset_id).values("check_name", "result").annotate(count=Count('id'))
    for cnt in counts:
        if cnt["check_name"] not in result:
            result[cnt["check_name"]] = {
                    "ok": 0,
                    "failed": 0,
                    "na": 0,
                    "application_count": 0,
                    "pass_count": 0,
            }

        if cnt["result"] is None:
            result[cnt["check_name"]]["na"] = cnt["count"]
        if cnt["result"] is True:
            result[cnt["check_name"]]["ok"] = cnt["count"]
        if cnt["result"] is False:
            result[cnt["check_name"]]["failed"] = cnt["count"]

    rates = ResourceLevelCheck.objects.filter(dataset=dataset_id).values("check_name").annotate(application_count=Sum('application_count')).annotate(pass_count=Sum('pass_count'))
    for rate in rates:
        result[rate["check_name"]]["application_count"] = rate["application_count"]
        result[rate["check_name"]]["pass_count"] = rate["pass_count"]
    return JsonResponse(result)
