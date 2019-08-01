from django.db.models import Count
from django.http import HttpResponse

from .models import ResourceLevelCheck


def resource_level_stats(request, dataset_id):
    distinct_checks = ResourceLevelCheck.objects.filter(dataset=dataset_id).values('check_name').distinct()

    result = []
    for check in distinct_checks:
        ok_count = 0
        failed_count = 0
        na_count = 0

        counts = ResourceLevelCheck.objects.filter(dataset=dataset_id).filter(check_name = check["check_name"]).values("result").annotate(count=Count('id'))
        for cnt in counts:
            if cnt["result"] is None:
                na_count = cnt["count"]
            if cnt["result"] is True:
                ok_count = cnt["count"]
            if cnt["result"] is False:
                failed_count = cnt["count"]
        check_stats = {
            "name": check["check_name"],
            "ok": ok_count,
            "failled": failed_count,
            "na": na_count,
        }
        result.append(check_stats)
    return HttpResponse(result)
