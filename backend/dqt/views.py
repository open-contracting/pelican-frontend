import random
import simplejson as json

from django.db.models import Count, Max, Min, Sum
from django.http import JsonResponse
from django.core import serializers
from django.db import connections

from .models import Dataset, DatasetLevelCheck, ResourceLevelCheck, Report
from .tools import ReservoirSampler


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


def field_level_path_stats(request, dataset_id, path):
    examples_cap = 20
    result = None

    with connections["data"].cursor() as cursor:
        cursor.execute(
            """
            select data->%s
            from report
            where dataset_id = %s and type = 'field_level_check';
            """, [path, dataset_id]
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse(
                {
                    "error": "no results for dataset_id: {}, path: '{}' combination".format(dataset_id, path)
                }
            )

        result = rows[0][0]

        # examples for this dataset_id, path combinations is cached
        if result["examples_filled"]:
            return JsonResponse(result)

        # coverage
        passed_coverage_sampler = ReservoirSampler(examples_cap)
        failed_coverage_sampler = ReservoirSampler(examples_cap)
        passed_coverage_checks_samplers = {}
        failed_coverage_checks_samplers = {}
        for check_name in result["coverage"]["checks"]:
            passed_coverage_checks_samplers[check_name] = ReservoirSampler(examples_cap)
            failed_coverage_checks_samplers[check_name] = ReservoirSampler(examples_cap)

        cursor.execute(
            """
            select sub1.meta, sub1.path, sub1.check
            from (
                select sub2.meta,
                        sub2.path->>'path' as path,
                        jsonb_array_elements(sub2.path->'coverage'->'check_results') as check
                from (
                    select result->'meta' as meta, jsonb_array_elements(d.value) as path
                    from field_level_check, jsonb_each(result->'checks') d
                    where dataset_id = %s and d.key = %s
                ) as sub2
                where sub2.path->'coverage'->>'check_results' is not null
            ) as sub1;
            """, [dataset_id, path]
        )

        while True:
            row = cursor.fetchone()
            if row is None:
                break

            example = {
                "meta": row[0],
                "path": row[1],
                "result": row[2]
            }

            if example["result"]["result"]:
                passed_coverage_sampler.process(example)
                passed_coverage_checks_samplers[example["result"]["name"]].process(example)
            else:
                failed_coverage_sampler.process(example)
                failed_coverage_checks_samplers[example["result"]["name"]].process(example)

        result["coverage"]["passed_examples"] = passed_coverage_sampler.retrieve_samples()
        result["coverage"]["failed_examples"] = failed_coverage_sampler.retrieve_samples()
        for check_name, sampler in passed_coverage_checks_samplers.items():
            result["coverage"]["checks"][check_name]["passed_examples"] = \
                passed_coverage_checks_samplers[check_name].retrieve_samples()
            result["coverage"]["checks"][check_name]["failed_examples"] = \
                failed_coverage_checks_samplers[check_name].retrieve_samples()

        # quality
        passed_quality_sampler = ReservoirSampler(examples_cap)
        failed_quality_sampler = ReservoirSampler(examples_cap)
        passed_quality_checks_samplers = {}
        failed_quality_checks_samplers = {}
        for check_name in result["quality"]["checks"]:
            passed_quality_checks_samplers[check_name] = ReservoirSampler(examples_cap)
            failed_quality_checks_samplers[check_name] = ReservoirSampler(examples_cap)

        cursor.execute(
            """
            select sub1.meta, sub1.path, sub1.check
            from (
                select sub2.meta,
                        sub2.path->>'path' as path,
                        jsonb_array_elements(sub2.path->'quality'->'check_results') as check
                from (
                    select result->'meta' as meta, jsonb_array_elements(d.value) as path
                    from field_level_check, jsonb_each(result->'checks') d
                    where dataset_id = %s and d.key = %s
                ) as sub2
                where sub2.path->'quality'->>'check_results' is not null
            ) as sub1;
            """, [dataset_id, path]
        )

        while True:
            row = cursor.fetchone()
            if row is None:
                break

            example = {
                "meta": row[0],
                "path": row[1],
                "result": row[2]
            }

            if example["result"]["result"]:
                passed_quality_sampler.process(example)
                passed_quality_checks_samplers[example["result"]["name"]].process(example)
            else:
                failed_quality_sampler.process(example)
                failed_quality_checks_samplers[example["result"]["name"]].process(example)

        result["quality"]["passed_examples"] = passed_quality_sampler.retrieve_samples()
        result["quality"]["failed_examples"] = failed_quality_sampler.retrieve_samples()
        for check_name, sampler in passed_quality_checks_samplers.items():
            result["quality"]["checks"][check_name]["passed_examples"] = \
                passed_quality_checks_samplers[check_name].retrieve_samples()
            result["quality"]["checks"][check_name]["failed_examples"] = \
                failed_quality_checks_samplers[check_name].retrieve_samples()

        # saving examples
        result["examples_filled"] = True
        cursor.execute(
            """
            update report
            set data = data || %s
            where dataset_id = %s and type = 'field_level_check';
            """, [json.dumps({path: result}), dataset_id]
        )

    return JsonResponse(result)
