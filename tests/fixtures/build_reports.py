"""
Rebuild reports.json from pelican-backend.sql.gz.

Run from the repository root:

    python tests/fixtures/build_reports.py

Each entry is a response that a view builds, so that a test can hand it to the serializer that describes it. The
entries are one per shape, with the example arrays cut to one entry each, to keep the file small.
"""

import copy
import gzip
import json
import re
from collections import defaultdict
from pathlib import Path

DUMP = Path("tests", "fixtures", "pelican-backend.sql.gz")
OUT = Path("tests", "fixtures", "reports.json")

# The only dataset with all six dataset-level meta shapes.
DATASET = 96
# The only dataset with time-based checks.
TIME_DATASET = 34
# A dataset whose collection metadata is set throughout, and the one whose publisher, OCID prefix, license and
# publication policy are null.
META_DATASET = 34
SPARSE_META_DATASET = 20

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
# The duration that a detail view adds to its response.
TIME = 0.05

ESCAPES = {"t": "\t", "n": "\n", "r": "\r", "\\": "\\"}


def unescape(value):
    """Return the value that COPY reads from the text."""
    if value == "\\N":
        return None
    return re.sub(r"\\(.)", lambda match: ESCAPES.get(match[1], match[1]), value)


def read_dump():
    """Return the dump's COPY statements as {table: [{column: value}]}."""
    tables = defaultdict(list)
    columns = {}
    table = None
    with gzip.open(DUMP, "rt") as f:
        for line in f:
            if line.startswith("COPY public."):
                table = line.split()[1].split(".")[1]
                columns[table] = re.search(r"\((.*?)\)", line).group(1).split(", ")
            elif table:
                if line.startswith("\\."):
                    table = None
                else:
                    values = [unescape(value) for value in line.rstrip("\n").split("\t")]
                    tables[table].append(dict(zip(columns[table], values, strict=True)))
    return tables


def rows(tables, table, dataset_id):
    for row in tables[table]:
        if row["dataset_id"] == str(dataset_id):
            yield row


def trim(value):
    """Cut every example array to one entry, and every distribution to one value, in place."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "examples" or key.endswith("_examples"):
                # A percentile check groups its examples by band.
                value[key] = child[:1] if isinstance(child, list) else {band: e[:1] for band, e in child.items()}
            elif isinstance(child, list) and key == "most_frequent":
                value[key] = trim(child[:1])
            elif isinstance(child, dict) and key == "shares":
                value[key] = trim(dict(list(child.items())[:1]))
            else:
                trim(child)
    elif isinstance(value, list):
        for child in value:
            trim(child)
    return value


def convert(value):
    """Return the column's value as a view returns it."""
    if value is None:
        return None
    if value in {"t", "f"}:
        return value == "t"
    if value.startswith("{"):
        return trim(json.loads(value))
    return int(value)


def report(tables, dataset_id, type):
    for row in rows(tables, "report", dataset_id):
        if row["type"] == type:
            return json.loads(row["data"])
    raise KeyError((dataset_id, type))


def examples(tables, table, dataset_id, key, name):
    for row in rows(tables, table, dataset_id):
        if row[key] == name:
            return trim(json.loads(row["data"]))
    raise KeyError((dataset_id, name))


def checks(tables, table, dataset_id, fields, names=None):
    """Return the report that get_report() builds from the check table."""
    return {
        row["check_name"]: {field: convert(row[field]) for field in fields}
        for row in rows(tables, table, dataset_id)
        if names is None or row["check_name"] in names
    }


def meta(tables, dataset_id):
    for row in tables["dataset"]:
        if row["id"] == str(dataset_id):
            return json.loads(row["meta"])
    raise KeyError(dataset_id)


def main():
    tables = read_dump()

    field_report = report(tables, DATASET, "field_level_check")
    resource_report = report(tables, DATASET, "resource_level_check")

    # FieldLevelDetail merges the examples into the report's entry, then adds the request's duration.
    field_detail = copy.deepcopy(field_report[FIELD_DETAIL])
    data = examples(tables, "field_level_check_examples", DATASET, "path", FIELD_DETAIL)
    for group in ("coverage", "quality"):
        field_detail[group]["passed_examples"] = data[group]["passed_examples"]
        field_detail[group]["failed_examples"] = data[group]["failed_examples"]
        for name, check in data[group]["checks"].items():
            field_detail[group]["checks"][name]["passed_examples"] = check["passed_examples"]
            field_detail[group]["checks"][name]["failed_examples"] = check["failed_examples"]
    field_detail["time"] = TIME

    # ResourceLevelDetail replaces the entry's example arrays with the examples row's, then does the same.
    resource_detail = copy.deepcopy(resource_report[RESOURCE_DETAIL])
    resource_detail.update(examples(tables, "resource_level_check_examples", DATASET, "check_name", RESOURCE_DETAIL))
    resource_detail["time"] = TIME

    OUT.write_text(
        json.dumps(
            {
                "field_level_report": {path: field_report[path] for path in FIELD_PATHS},
                "field_level_detail": field_detail,
                "compiled_release_level_report": {name: resource_report[name] for name in RESOURCE_NAMES},
                "compiled_release_level_detail": resource_detail,
                "dataset_level_report": checks(
                    tables, "dataset_level_check", DATASET, ("result", "value", "meta"), DATASET_NAMES
                ),
                # The whole report, since the only dataset with time-based checks has three of them.
                "time_based_report": checks(
                    tables,
                    "time_variance_level_check",
                    TIME_DATASET,
                    ("coverage_value", "coverage_result", "check_value", "check_result", "meta"),
                ),
                "dataset_meta": meta(tables, META_DATASET),
                "dataset_meta_sparse": meta(tables, SPARSE_META_DATASET),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
