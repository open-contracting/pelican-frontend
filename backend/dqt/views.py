import random

from django.db.models import Count, Max, Min, Sum
from django.http import JsonResponse
from django.core import serializers

from .models import Dataset, DatasetLevelCheck, ResourceLevelCheck


def dataset_stats(request, dataset_id):
    result = {}
    dataset_meta = Dataset.objects.get(id=dataset_id)
    result["name"] = dataset_meta.name
    result["meta"] = dataset_meta.meta

    return JsonResponse(result)


def resource_level_stats(request, dataset_id):
    result = {}

    counts = ResourceLevelCheck.objects.filter(
        dataset=dataset_id).values(
        "check_name", "result").annotate(
        count=Count('id'))
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

    rates = ResourceLevelCheck.objects.filter(
        dataset=dataset_id).values("check_name").annotate(
        application_count=Sum('application_count')).annotate(
        pass_count=Sum('pass_count'))
    for rate in rates:
        result[rate["check_name"]]["application_count"] = rate["application_count"]
        result[rate["check_name"]]["pass_count"] = rate["pass_count"]

    for key, item in result.items():
        max_id = ResourceLevelCheck.objects.filter(
            check_name=key).filter(
            dataset=dataset_id).aggregate(
            max_id=Max("id"))["max_id"]

        min_id = ResourceLevelCheck.objects.filter(
            check_name=key).filter(
            dataset=dataset_id).aggregate(
            min_id=Min("id"))["min_id"]

        rand_id = random.randint(min_id, min_id + (max_id - min_id))

        passed_examples = ResourceLevelCheck.objects.filter(
            check_name=key).filter(
            dataset=dataset_id).filter(result=True).filter(id__gt=rand_id)[:5]

        result[key]["examples"] = {}
        result[key]["examples"]["passed"] = []
        for item in passed_examples:
            val = {}
            val["meta"] = item.meta
            val["data"] = item.data_item.data
            result[key]["examples"]["passed"].append(val)

        failed_examples = ResourceLevelCheck.objects.filter(
            check_name=key).filter(
            dataset=dataset_id).filter(result=False).filter(id__gt=rand_id)[:5]

        result[key]["examples"]["failed"] = []
        for item in failed_examples:
            val = {}
            val["meta"] = item.meta
            val["data"] = item.data_item.data
            result[key]["examples"]["failed"].append(val)

    return JsonResponse(result)


def dataset_level_stats(request, dataset_id):
    result = {}
    checks = DatasetLevelCheck.objects.filter(
        dataset=dataset_id)
    for check in checks:
        result[check.check_name] = {
            "result": check.result,
            "value": check.value,
            "meta": check.meta,
        }
    return JsonResponse(result)
