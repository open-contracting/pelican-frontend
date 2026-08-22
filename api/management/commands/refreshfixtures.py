"""
Rebuild both test fixtures from the Pelican backend database that PELICAN_BACKEND_DATABASE_URL names.

They are written in one pass, so that the report entries cannot drift from the dump they are taken from:

-  ``tests/fixtures/pelican-backend.sql.gz``, the database to develop against
-  ``tests/fixtures/reports.json``, the responses that ``tests/api/test_serializers.py`` checks

The rows are copied as they are, with no scrubbing. A report is an aggregate of the data items it is about, so
replacing a publisher's name or an OCID would decouple the two: the check results, charts and examples would no
longer follow from the data on display. Choose datasets whose publishers publish openly.

The dump is kept small by copying only the data items that the surviving examples point to, so that every example can
still be previewed. A report's counts are over the whole dataset, and are left alone, so they exceed the number of
data items copied.
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

JSON_OIDS = {types["json"].oid, types["jsonb"].oid}

# 96 is the only dataset with all six dataset-level meta shapes. 34 is the only one with time-based checks, whose
# examples pair its data items with its ancestor's, so 25 is here too. 20 is the only filtered dataset whose
# collection metadata is null, and 17 is the parent that the dataset picker names. 44 stopped before its reports were
# written, so it has no Pelican metadata, and it is the only one that declares extensions.
DATASETS = [17, 20, 25, 34, 44, 96]
# The number of examples to keep per array, which is one section of a detail page. Each costs a data item, so this is
# a sample, not the up-to-50 that a page shows: ExampleBoxes.vue only collapses a section above five entries.
EXAMPLES = 3
# A field-level check row holds every check of one data item, at about 90 kB, so the two tables that only the failure
# downloads read are copied for the lowest CHECKED data items of each dataset, rather than for all of them. The
# downloads therefore list fewer OCIDs than the reports count.
CHECKED = 50

# The tables whose JSON holds the example arrays, and so decides which data items to copy.
EXAMPLE_TABLES = (
    "field_level_check_examples",
    "resource_level_check_examples",
    "dataset_level_check",
    "time_variance_level_check",
    "report",
)
# The tables that the entries of reports.json are taken from.
ENTRY_TABLES = (*EXAMPLE_TABLES, "dataset")
# The column that each table is filtered on. The order is the order in which the tables are written, which the
# foreign keys constrain, since the schema declares them before the data is copied.
CONDITIONS = {
    "dataset": "id = ANY(%(datasets)s)",
    "dataset_filter": "dataset_id_filtered = ANY(%(datasets)s) AND dataset_id_original = ANY(%(datasets)s)",
    "progress_monitor_dataset": "dataset_id = ANY(%(datasets)s)",
    "data_item": "id = ANY(%(items)s)",
    "progress_monitor_item": "item_id = ANY(%(items)s)",
    "field_level_check": "data_item_id = ANY(%(checked)s)",
    "resource_level_check": "data_item_id = ANY(%(checked)s)",
    "field_level_check_examples": "dataset_id = ANY(%(datasets)s)",
    "resource_level_check_examples": "dataset_id = ANY(%(datasets)s)",
    "dataset_level_check": "dataset_id = ANY(%(datasets)s)",
    "time_variance_level_check": "dataset_id = ANY(%(datasets)s)",
    "report": "dataset_id = ANY(%(datasets)s)",
    # The frontend reads no exchange rate, and Pelican backend writes one per currency per day.
    "exchange_rates": "false",
}
SCHEMA_END = "--\n-- PostgreSQL database dump complete\n--\n\n"

# reports.json holds one entry per shape that api/serializers.py describes, each being the response that a view
# builds, so that a test can hand it to the serializer. Its example arrays are cut to one entry, to keep it small.
#
# Two field-level checks: one whose quality group has checks, one whose quality group has none.
FIELD_PATHS = ("ocid", "id")
# The only path whose four example arrays are all non-empty.
FIELD_DETAIL = "parties.contactPoint.telephone"
# Two compiled release-level checks, and one detail whose three example kinds are all non-empty.
RESOURCE_NAMES = ("coherent.dates", "coherent.tender_status")
RESOURCE_DETAIL = "coherent.tender_status"
# One dataset-level check per meta shape: code (shares), top 3 (most_frequent), numeric (total_processed),
# percentile (sums), biggest share (ocid_share), single value share (total_unique_count), and a check that could not
# run (reason).
DATASET_NAMES = (
    "distribution.tender_status",
    "distribution.tender_value_repetition",
    "misc.url_availability",
    "distribution.tender_value",
    "distribution.buyer_repetition",
    "distribution.buyer",
    "distribution.contracts_status",
)
# The dataset that the entries above are taken from, and the only one with time-based checks.
ENTRY_DATASET = 96
TIME_DATASET = 34
# A dataset whose collection metadata is set throughout, the one whose publisher, OCID prefix, license and publication
# policy are null, and the one that stopped before Pelican wrote its metadata.
META_DATASETS = {"dataset_meta": 34, "dataset_meta_sparse": 20, "dataset_meta_in_progress": 44}
# The duration that a detail view adds to its response.
TIME = 0.05


def trim(value, count, *, distributions=False):
    """Cut every example array to count entries, and every distribution to one value, in place."""
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


def schema():
    """Return the database's schema, as pg_dump writes it."""
    database = settings.DATABASES["pelican_backend"]
    # btree_gin is the only extension the schema needs: a report's index spans a text column and a JSON column.
    arguments = ["pg_dump", "--schema-only", "--no-owner", "--no-privileges", "--extension=btree_gin"]
    for option, key in (("--host", "HOST"), ("--port", "PORT"), ("--username", "USER"), ("--dbname", "NAME")):
        if database[key]:
            arguments.extend([option, str(database[key])])

    environment = os.environ.copy()
    if database["PASSWORD"]:
        environment["PGPASSWORD"] = database["PASSWORD"]
    stdout = subprocess.run(  # noqa: S603 # constants and settings
        arguments, check=True, capture_output=True, text=True, env=environment
    ).stdout

    text, marker, _ = stdout.partition(SCHEMA_END)
    if not marker:
        sys.exit("pg_dump wrote an unexpected ending")
    # The token in the \restrict command that guards the rest of the file is random, and would otherwise change the
    # fixture on every rebuild. Its \unrestrict command follows the ending, and is dropped with it.
    return re.sub(r"\\restrict \S+\n\n", "", text)


def select(cursor, table, **parameters):
    """Return the table's matching rows, in ID order, as (columns, rows), with the JSON columns decoded."""
    cursor.execute(f"SELECT * FROM {table} WHERE {CONDITIONS[table]} ORDER BY id", parameters)  # noqa: S608 # constant
    # Django's backend reads a JSON column as text, since a model's field decodes it. There is no model here.
    indices = {index for index, column in enumerate(cursor.description) if column.type_code in JSON_OIDS}
    rows = [
        [json.loads(value) if index in indices and value is not None else value for index, value in enumerate(row)]
        for row in cursor
    ]
    return [column[0] for column in cursor.description], rows


def dump(table, columns, rows):
    """Yield the table's COPY statement, then the statement that sets its sequence."""
    yield f"--\n-- Data for Name: {table}; Type: TABLE DATA; Schema: public; Owner: -\n--\n\n"
    yield f"COPY public.{table} ({', '.join(columns)}) FROM stdin;\n"
    for row in rows:
        yield "\t".join(literal(value) for value in row) + "\n"
    yield "\\.\n\n\n"

    # A row inserted into the loaded database must not collide with a copied row.
    last = max((row[columns.index("id")] for row in rows), default=0)
    yield f"--\n-- Name: {table}_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -\n--\n\n"
    yield f"SELECT pg_catalog.setval('public.{table}_id_seq', {last or 1}, {'true' if last else 'false'});\n\n\n"


def one(rows, **conditions):
    """Return the one row matching the conditions."""
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


def entries(tables):
    """Return the entries of reports.json."""
    field = one(tables["report"], dataset_id=ENTRY_DATASET, type="field_level_check")["data"]
    resource = one(tables["report"], dataset_id=ENTRY_DATASET, type="resource_level_check")["data"]

    # FieldLevelDetail merges the examples into the report's entry, then adds the request's duration.
    field_detail = copy.deepcopy(field[FIELD_DETAIL])
    data = one(tables["field_level_check_examples"], dataset_id=ENTRY_DATASET, path=FIELD_DETAIL)["data"]
    for group in ("coverage", "quality"):
        field_detail[group]["passed_examples"] = data[group]["passed_examples"][:1]
        field_detail[group]["failed_examples"] = data[group]["failed_examples"][:1]
        for name, check in data[group]["checks"].items():
            field_detail[group]["checks"][name]["passed_examples"] = check["passed_examples"][:1]
            field_detail[group]["checks"][name]["failed_examples"] = check["failed_examples"][:1]
    field_detail["time"] = TIME

    # ResourceLevelDetail replaces the entry's example arrays with the examples row's, then does the same.
    resource_detail = copy.deepcopy(resource[RESOURCE_DETAIL])
    examples = one(tables["resource_level_check_examples"], dataset_id=ENTRY_DATASET, check_name=RESOURCE_DETAIL)
    resource_detail.update(trim(examples["data"], 1))
    resource_detail["time"] = TIME

    return {
        "field_level_report": {path: field[path] for path in FIELD_PATHS},
        "field_level_detail": field_detail,
        "compiled_release_level_report": {name: resource[name] for name in RESOURCE_NAMES},
        "compiled_release_level_detail": resource_detail,
        "dataset_level_report": checks(
            tables["dataset_level_check"], ENTRY_DATASET, ("result", "value", "meta"), DATASET_NAMES
        ),
        # The whole report, since the only dataset with time-based checks has three of them.
        "time_based_report": checks(
            tables["time_variance_level_check"],
            TIME_DATASET,
            ("coverage_value", "coverage_result", "check_value", "check_result", "meta"),
        ),
        **{
            key: trim(one(tables["dataset"], id=dataset_id)["meta"], 1, distributions=True)
            for key, dataset_id in META_DATASETS.items()
        },
    }


class Command(BaseCommand):
    help = "Rebuild the test fixtures from a Pelican backend database"

    def handle(self, *args, **options):
        text = [schema()]
        tables = {}

        with connections["pelican_backend"].cursor() as cursor:
            # The example arrays are trimmed before the data items are chosen, so that only the surviving examples
            # count towards the file's size.
            selected = {table: select(cursor, table, datasets=DATASETS) for table in EXAMPLE_TABLES}

            item_ids = set()
            for columns, rows in selected.values():
                index = columns.index("data" if "data" in columns else "meta")
                for row in rows:
                    add_data_item_ids(trim(row[index], EXAMPLES), item_ids)

            cursor.execute("SELECT id, dataset_id FROM data_item WHERE id = ANY(%(ids)s)", {"ids": sorted(item_ids)})
            found = dict(cursor.fetchall())
            if missing := item_ids - set(found):
                sys.exit(f"{len(missing)} examples point to deleted data items, like {min(missing)}")
            if orphans := {item_id for item_id, dataset_id in found.items() if dataset_id not in DATASETS}:
                sys.exit(f"{len(orphans)} examples point to data items of an uncopied dataset, like {min(orphans)}")
            items = sorted(item_ids)

            by_dataset = defaultdict(list)
            for item_id in items:
                by_dataset[found[item_id]].append(item_id)
            checked = sorted(item_id for dataset_items in by_dataset.values() for item_id in dataset_items[:CHECKED])

            for table in CONDITIONS:
                columns, rows = selected.get(table) or select(
                    cursor, table, datasets=DATASETS, items=items, checked=checked
                )
                text.extend(dump(table, columns, rows))
                if table in ENTRY_TABLES:
                    tables[table] = [dict(zip(columns, row, strict=True)) for row in rows]

        text.append(SCHEMA_END)

        # The dump is written before the entries are taken, since taking one trims the rows it comes from further.
        directory = settings.BASE_DIR / "tests" / "fixtures"
        dump_path = directory / "pelican-backend.sql.gz"
        dump_path.write_bytes(gzip.compress("".join(text).encode(), compresslevel=9, mtime=0))
        (directory / "reports.json").write_text(json.dumps(entries(tables), indent=2, sort_keys=True) + "\n")

        self.stdout.write(
            f"{dump_path.name}: {dump_path.stat().st_size:,} bytes, "
            f"{len(items):,} data items, {len(checked):,} checked"
        )
