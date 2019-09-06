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


def field_level_stats(request, dataset_id):
    with connections["data"].cursor() as cursor:
        cursor.execute(
            """
            select data
            from report
            where dataset_id = %s and type = 'field_level_check';
            """, [dataset_id]
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse(
                {
                    "error": "no field_level_check report for dataset_id: {}".format(dataset_id)
                }
            )

        return JsonResponse(rows[0][0])


def field_level_path_stats(request, dataset_id, path):
    examples_cap = 20
    result = None

    with connections["data"].cursor() as cursor:
        cursor.execute(
            """
            select data->%s
            from report
            where dataset_id = %s and
                  type = 'field_level_check' and
                  data ? %s;
            """, [path, dataset_id, path]
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


def resource_level_stats(request, dataset_id):
    with connections["data"].cursor() as cursor:
        cursor.execute(
            """
            select data
            from report
            where dataset_id = %s and type = 'resource_level_check';
            """, [dataset_id]
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse(
                {
                    "error": "no resource_level_check report for dataset_id: {}".format(dataset_id)
                }
            )

        return JsonResponse(rows[0][0])


def resource_level_check_name_stats(request, dataset_id, check_name):
    examples_cap = 20
    result = None

    with connections["data"].cursor() as cursor:
        cursor.execute(
            """
            select data->%s
            from report
            where dataset_id = %s and
                  type = 'resource_level_check' and
                  data ? %s;
            """, [check_name, dataset_id, check_name]
        )
        rows = cursor.fetchall()

        if not rows:
            return JsonResponse(
                {
                    "error": "no results for dataset_id: {}, check_name: '{}' combination".format(
                        dataset_id,
                        check_name
                    )
                }
            )

        result = rows[0][0]

        # examples for this dataset_id, check_name combinations is cached
        if result["examples_filled"]:
            return JsonResponse(result)

        # picking examples
        passed_sampler = ReservoirSampler(examples_cap)
        failed_sampler = ReservoirSampler(examples_cap)
        undefined_sampler = ReservoirSampler(examples_cap)

        cursor.execute(
            """
            select result->'meta' as meta, result->'checks'->%s as result
            from resource_level_check
            where dataset_id = %s;
            """, [check_name, dataset_id]
        )

        while True:
            row = cursor.fetchone()
            if row is None:
                break

            example = {
                "meta": row[0],
                "result": row[1]
            }

            if example["result"]["result"] is True:
                passed_sampler.process(example)
            elif example["result"]["result"] is False:            
                failed_sampler.process(example)
            elif example["result"]["result"] is None:
                undefined_sampler.process(example)
            else:
                raise ValueError()

        result["passed_examples"] = passed_sampler.retrieve_samples()
        result["failed_examples"] = failed_sampler.retrieve_samples()
        result["undefined_examples"] = undefined_sampler.retrieve_samples()

        # saving examples
        result["examples_filled"] = True
        cursor.execute(
            """
            update report
            set data = data || %s
            where dataset_id = %s and type = 'resource_level_check';
            """, [json.dumps({check_name: result}), dataset_id]
        )

    return JsonResponse(result)
