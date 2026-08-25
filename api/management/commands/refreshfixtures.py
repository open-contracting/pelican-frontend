"""
Rebuild fixtures from the ``PELICAN_BACKEND_DATABASE_URL`` database.

-  ``tests/fixtures/pelican-backend.sql.gz`` is a sample database to develop against
-  ``tests/fixtures/reports.json`` is used to test serializers

The dump is kept small by copying only the data items that the surviving examples point to.
"""

import copy
import gzip
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections
from psycopg.postgres import types

# Input configuration #

# Change these when a dataset is deleted from the database, or when Pelican backend writes a shape that none of them
# covers: each comment states the criterion to search for a replacement.

# A dataset with all six dataset-level `meta` shapes.
# A dataset with a code chart with more values than it draws bars for.
# A dataset from which to take all field-level, compiled release-level and dataset-level reports.json entries.
ENTRY_DATASET = 96

# A dataset with time-based checks, without which the /time/:datasetId routes are unreachable.
# A dataset whose collection metadata is set throughout, for dataset_meta.
TIME_DATASET = 34

# A filtered dataset, without which the picker's tree and a filter's message are unreachable.
# A dataset whose publisher, OCID prefix, license and publication policy are null, for dataset_meta_sparse.
SPARSE_DATASET = 20

# A dataset that stopped before its reports were written, so that a page can be missing its report.
# A dataset for which Pelican wrote no metadata, for dataset_meta_in_progress.
# A dataset that declares extensions.
IN_PROGRESS_DATASET = 44

# The datasets to copy. Each one's ancestor and parent are copied, too.
DATASETS = [ENTRY_DATASET, TIME_DATASET, SPARSE_DATASET, IN_PROGRESS_DATASET]
# The dataset behind each reports.json entry that holds a dataset's `meta`.
META_DATASETS = {
    "dataset_meta": TIME_DATASET,
    "dataset_meta_sparse": SPARSE_DATASET,
    "dataset_meta_in_progress": IN_PROGRESS_DATASET,
}
# Two field-level checks: one whose quality group has checks, one whose quality group has none.
FIELD_CHECK_PATHS = ("ocid", "id")
# A path whose four example arrays are all non-empty.
FIELD_DETAIL = "parties.contactPoint.telephone"
# Two compiled release-level checks.
RESOURCE_CHECK_NAMES = ("coherent.dates", "coherent.tender_status")
# A check whose three example kinds are all non-empty.
RESOURCE_DETAIL = "coherent.tender_status"
# One dataset-level check per `meta` shape: code (shares), top 3 (most_frequent), numeric (total_processed), percentile
# (sums), biggest share (ocid_share), single value share (total_unique_count), and a check that could not run (reason).
DATASET_CHECK_NAMES = (
    "distribution.tender_status",
    "distribution.tender_value_repetition",
    "misc.url_availability",
    "distribution.tender_value",
    "distribution.buyer_repetition",
    "distribution.buyer",
    "distribution.contracts_status",
)

# Command configuration #

# An array is one section of a detail page. Each costs a data item. 6 fills a section past the 5 entries above which
# ExampleBoxes.vue collapses.
EXAMPLES_PER_ARRAY = 6
# The rows to copy from field_level_check, and from resource_level_check. Pelican backend writes one row of each
# per data item, and a field-level row is about 75 kB, holding every check of that item, so copying them all would
# multiply the dump's size. This limit causes the `{field_level,compiled_release_level}/:name/failures/` endpoints
# (the only readers of those tables) to return fewer OCIDs than the reports count.
CHECK_ROWS_PER_DATASET = 50
# The tables whose `data` or `meta` column stores the example arrays. Those examples point to the data items to copy.
EXAMPLE_TABLES = (
    "field_level_check_examples",
    "resource_level_check_examples",
    "dataset_level_check",
    "time_variance_level_check",
)
# The tables from which the reports.json entries are taken.
ENTRY_TABLES = (*EXAMPLE_TABLES, "report", "dataset")
# The WHERE clause that selects each table's rows. The tables are written in this order to respect foreign keys.
CONDITIONS = {
    "dataset": "id = ANY(%(datasets)s)",
    "dataset_filter": "dataset_id_filtered = ANY(%(datasets)s) AND dataset_id_original = ANY(%(datasets)s)",
    "progress_monitor_dataset": "dataset_id = ANY(%(datasets)s)",
    "data_item": "id = ANY(%(items)s)",
    "progress_monitor_item": "item_id = ANY(%(items)s)",
    "field_level_check": "data_item_id = ANY(%(items_with_check_rows)s)",
    "resource_level_check": "data_item_id = ANY(%(items_with_check_rows)s)",
    "field_level_check_examples": "dataset_id = ANY(%(datasets)s)",
    "resource_level_check_examples": "dataset_id = ANY(%(datasets)s)",
    "dataset_level_check": "dataset_id = ANY(%(datasets)s)",
    "time_variance_level_check": "dataset_id = ANY(%(datasets)s)",
    "report": "dataset_id = ANY(%(datasets)s)",
    # The frontend reads no exchange rate.
    "exchange_rates": "false",
}
# The end of a pg_dump file, after which its \unrestrict command follows.
SCHEMA_END = "--\n-- PostgreSQL database dump complete\n--\n\n"
# The duration that a detail view adds to its response.
TIME = 0.05
# Django's backend reads a JSON column as text, since a model's field decodes it. There is no model here.
JSON_OIDS = {types["json"].oid, types["jsonb"].oid}


def trim(value, count, *, distributions=False):
    """Cut every example array to ``count`` entries, in place, and every distribution to one value if requested."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "examples" or key.endswith("_examples"):
                # A percentile check groups its examples by band.
                if isinstance(child, list):
                    value[key] = child[:count]
                elif isinstance(child, dict):
                    value[key] = {band: examples[:count] for band, examples in child.items()}
            elif distributions and isinstance(child, list) and key in {"most_frequent", "extensions"}:
                value[key] = trim(child[:1], count, distributions=True)
            elif distributions and isinstance(child, dict) and key == "shares":
                value[key] = trim(dict(list(child.items())[:1]), count, distributions=True)
            else:
                trim(child, count, distributions=distributions)
    elif isinstance(value, list):
        for child in value:
            trim(child, count, distributions=distributions)
    return value


def add_data_item_ids(value, ids):
    """Add the IDs of the data items that the examples point to."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"item_id", "new_item_id"} and isinstance(child, int):
                ids.add(child)
            else:
                add_data_item_ids(child, ids)
    elif isinstance(value, list):
        for child in value:
            add_data_item_ids(child, ids)


def literal(value):
    """Return the value in the text format that COPY reads."""
    if value is None:
        return "\\N"
    if isinstance(value, bool):
        return "t" if value else "f"
    if isinstance(value, int | float):
        return str(value)
    if isinstance(value, dict | list):
        value = json.dumps(value, ensure_ascii=False)
    elif isinstance(value, datetime | date):
        value = str(value)
    return value.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")


def select(cursor, table, **parameters):
    """Return the table's matching rows, in ID order, as (columns, rows), with the JSON columns decoded."""
    cursor.execute(f"SELECT * FROM {table} WHERE {CONDITIONS[table]} ORDER BY id", parameters)  # noqa: S608 # constant
    indices = {index for index, column in enumerate(cursor.description) if column.type_code in JSON_OIDS}
    rows = [
        [json.loads(value) if index in indices and value is not None else value for index, value in enumerate(row)]
        for row in cursor
    ]
    return [column[0] for column in cursor.description], rows


def one(rows, **conditions):
    """Return the first row matching all the conditions."""
    for row in rows:
        if all(row[column] == value for column, value in conditions.items()):
            return row
    raise KeyError(conditions)


def checks(rows, dataset_id, fields, names=None):
    """Return the report that get_report() builds from a check table's rows."""
    return {
        row["check_name"]: {field: trim(row[field], 1, distributions=True) for field in fields}
        for row in rows
        if row["dataset_id"] == dataset_id and (names is None or row["check_name"] in names)
    }


class Command(BaseCommand):
    help = "Rebuild fixtures from the PELICAN_BACKEND_DATABASE_URL database"

    def handle(self, *args, **options):
        # Prepare the pg_dump command.
        database = settings.DATABASES["pelican_backend"]
        arguments = ["pg_dump", "--schema-only", "--no-owner", "--no-privileges", "--extension=btree_gin"]
        for option, key in (("--host", "HOST"), ("--port", "PORT"), ("--username", "USER"), ("--dbname", "NAME")):
            if database[key]:
                arguments.extend([option, str(database[key])])
        environment = os.environ.copy()
        if database["PASSWORD"]:
            environment["PGPASSWORD"] = database["PASSWORD"]

        # Pre-process the pg_dump output. The token in pg_dump's `\restrict` and `\unrestrict` commands is random,
        # so both are cut, so that a re-run writes the same bytes. Remove both, plus everything after the ending.
        stdout = subprocess.run(  # noqa: S603 # constants and settings
            arguments, check=True, capture_output=True, text=True, env=environment
        ).stdout
        schema, marker, _ = stdout.partition(SCHEMA_END)
        if not marker:
            sys.exit("pg_dump wrote an unexpected ending")
        text = [re.sub(r"\\restrict \S+\n\n", "", schema)]

        tables = {}
        with connections["pelican_backend"].cursor() as cursor:
            # A deleted dataset is skipped, rather than fatal, so that the rest can be refreshed before a replacement
            # is found. Its `meta` entry is then absent, and test_dataset_meta fails on it.
            cursor.execute("SELECT id FROM dataset WHERE id = ANY(%(ids)s)", {"ids": DATASETS})
            chosen = [row[0] for row in cursor]
            if deleted := sorted(set(DATASETS) - set(chosen)):
                message = f"datasets {deleted} are deleted: choose replacements meeting the same criteria"
                # Every reports.json entry but a `meta` one is taken from these two datasets.
                if {ENTRY_DATASET, TIME_DATASET}.intersection(deleted):
                    sys.exit(message)
                self.stderr.write(self.style.WARNING(message))

            # A time-based example pairs a data item with its ancestor's, and the picker names a filtered dataset's
            # parent, so both are copied alongside the chosen datasets.
            cursor.execute(
                """
                SELECT ancestor_id FROM dataset WHERE id = ANY(%(ids)s) AND ancestor_id IS NOT NULL
                UNION
                SELECT dataset_id_original FROM dataset_filter WHERE dataset_id_filtered = ANY(%(ids)s)
                """,
                {"ids": chosen},
            )
            datasets = sorted({*chosen, *(row[0] for row in cursor)})

            # SELECT the example tables, whose rows are used for the sample dump and reports.json entries.
            selected = {table: select(cursor, table, datasets=datasets) for table in EXAMPLE_TABLES}

            # Trim the example arrays, then collect the data items that the surviving examples point to, so that a
            # cut example contributes nothing towards the dump's size.
            item_ids = set()
            for columns, rows in selected.values():
                index = columns.index("data" if "data" in columns else "meta")
                for row in rows:
                    add_data_item_ids(trim(row[index], EXAMPLES_PER_ARRAY), item_ids)

            # SELECT the data items.
            cursor.execute("SELECT id, dataset_id FROM data_item WHERE id = ANY(%(ids)s)", {"ids": sorted(item_ids)})
            found = dict(cursor.fetchall())
            if missing := item_ids - set(found):
                sys.exit(f"{len(missing)} examples point to deleted data items, like {min(missing)}")
            if orphans := {item_id for item_id, dataset_id in found.items() if dataset_id not in datasets}:
                sys.exit(f"{len(orphans)} examples point to data items of an uncopied dataset, like {min(orphans)}")
            items = sorted(item_ids)

            # Cap the data items whose checks are copied, taking the lowest IDs, so that a rebuild takes the same ones.
            by_dataset = defaultdict(list)
            for item_id in items:
                by_dataset[found[item_id]].append(item_id)
            items_with_check_rows = sorted(
                item_id for dataset_items in by_dataset.values() for item_id in dataset_items[:CHECK_ROWS_PER_DATASET]
            )

            # Add table data to the sample dump.
            for table in CONDITIONS:
                columns, rows = selected.get(table) or select(
                    cursor, table, datasets=datasets, items=items, items_with_check_rows=items_with_check_rows
                )

                text.append(f"--\n-- Data for Name: {table}; Type: TABLE DATA; Schema: public; Owner: -\n--\n\n")
                text.append(f"COPY public.{table} ({', '.join(columns)}) FROM stdin;\n")
                text.extend("\t".join(literal(value) for value in row) + "\n" for row in rows)
                text.append("\\.\n\n\n")

                # A row inserted into the loaded database must not collide with a copied row.
                last = max((row[columns.index("id")] for row in rows), default=0)
                text.append(f"--\n-- Name: {table}_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -\n--\n\n")
                text.append(
                    f"SELECT pg_catalog.setval('public.{table}_id_seq', {last or 1}, "
                    f"{'true' if last else 'false'});\n\n\n"
                )

                if table in ENTRY_TABLES:
                    tables[table] = [dict(zip(columns, row, strict=True)) for row in rows]

        text.append(SCHEMA_END)

        # Building a reports.json entry trims its row's arrays to one entry, in place, so the dump is written first.
        directory = settings.BASE_DIR / "tests" / "fixtures"
        dump = directory / "pelican-backend.sql.gz"
        dump.write_bytes(gzip.compress("".join(text).encode(), compresslevel=9, mtime=0))

        # An entry keeps one example per array, which is all a serializer needs, and all a reader of the file reads.
        field = one(tables["report"], dataset_id=ENTRY_DATASET, type="field_level_check")["data"]
        resource = one(tables["report"], dataset_id=ENTRY_DATASET, type="resource_level_check")["data"]

        # The FieldLevelDetail view copies the field_level_check_examples row's arrays into the path's entry in the
        # report, group-by-group and check-by-check, then adds the request's duration.
        field_detail = copy.deepcopy(field[FIELD_DETAIL])
        data = one(tables["field_level_check_examples"], dataset_id=ENTRY_DATASET, path=FIELD_DETAIL)["data"]
        for group in ("coverage", "quality"):
            field_detail[group]["passed_examples"] = data[group]["passed_examples"][:1]
            field_detail[group]["failed_examples"] = data[group]["failed_examples"][:1]
            for name, check in data[group]["checks"].items():
                field_detail[group]["checks"][name]["passed_examples"] = check["passed_examples"][:1]
                field_detail[group]["checks"][name]["failed_examples"] = check["failed_examples"][:1]
        field_detail["time"] = TIME

        # The ResourceLevelDetail view updates the check's entry in the report with the resource_level_check_examples
        # row, whose keys are the three example arrays, then adds the request's duration.
        resource_detail = copy.deepcopy(resource[RESOURCE_DETAIL])
        examples = one(tables["resource_level_check_examples"], dataset_id=ENTRY_DATASET, check_name=RESOURCE_DETAIL)
        resource_detail.update(trim(examples["data"], 1))
        resource_detail["time"] = TIME

        entries = {
            "field_level_report": {path: field[path] for path in FIELD_CHECK_PATHS},
            "field_level_detail": field_detail,
            "compiled_release_level_report": {name: resource[name] for name in RESOURCE_CHECK_NAMES},
            "compiled_release_level_detail": resource_detail,
            "dataset_level_report": checks(
                tables["dataset_level_check"],
                ENTRY_DATASET,
                ("result", "value", "meta"),
                DATASET_CHECK_NAMES,
            ),
            "time_based_report": checks(
                tables["time_variance_level_check"],
                TIME_DATASET,
                ("coverage_value", "coverage_result", "check_value", "check_result", "meta"),
                # Copy the entire report, being three checks.
            ),
            **{
                key: trim(one(tables["dataset"], id=dataset_id)["meta"], 1, distributions=True)
                for key, dataset_id in META_DATASETS.items()
                if dataset_id in chosen
            },
        }
        if not entries["time_based_report"]:
            sys.exit(f"dataset {TIME_DATASET} has no time-based checks: choose a replacement")
        if absent := set(DATASET_CHECK_NAMES) - set(entries["dataset_level_report"]):
            sys.exit(f"dataset {ENTRY_DATASET} has no {', '.join(sorted(absent))}: choose a replacement per shape")

        (directory / "reports.json").write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n")

        self.stdout.write(
            f"{dump.name}: {dump.stat().st_size:,} bytes, {len(items):,} data items, "
            f"{len(items_with_check_rows):,} with check rows, from datasets {', '.join(map(str, datasets))}"
        )
