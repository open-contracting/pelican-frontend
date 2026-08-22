"""
Rebuild pelican-backend.sql.gz from a Pelican backend database, set as PELICAN_BACKEND_DATABASE_URL.

Run from the repository root:

    PELICAN_BACKEND_DATABASE_URL=... python tests/fixtures/build_dump.py

The rows are copied as they are, because a report is an aggregate of the data items it is about, and editing either
would decouple the two. Every example array is cut to EXAMPLES entries, and the only data items copied are the ones
the surviving examples point to, which is what keeps the file small.
"""

import gzip
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

import psycopg

# 96 is the only dataset with all six dataset-level meta shapes. 34 is the only one with time-based checks, whose
# examples pair its data items with its ancestor's, so 25 is here too. 20 is the only filtered dataset whose
# collection metadata is null, and 17 is the parent that the dataset picker names. 44 stopped before its reports were
# written, so it has no Pelican metadata, and it is the only one that declares extensions.
DATASETS = [17, 20, 25, 34, 44, 96]
# The number of examples to keep per array, which is one section of a detail page. Each costs a data item, so this is
# a sample, not the up-to-50 that a page shows: ExampleBoxes.vue only collapses a section above five entries.
EXAMPLES = 3
# A field-level check row holds every check of one data item, at about 90 kB, so the two tables that only the failure
# downloads read are copied for the lowest CHECKED data items of each dataset, rather than for all of them.
CHECKED = 50

OUT = Path("tests", "fixtures", "pelican-backend.sql.gz")
# The tables whose JSON holds the example arrays, and so decides which data items to copy.
EXAMPLE_TABLES = (
    "field_level_check_examples",
    "resource_level_check_examples",
    "dataset_level_check",
    "time_variance_level_check",
    "report",
)
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


def trim(value):
    """Cut every example array to EXAMPLES entries, in place, and return the value."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key != "examples" and not key.endswith("_examples"):
                trim(child)
            elif isinstance(child, list):
                value[key] = child[:EXAMPLES]
            elif isinstance(child, dict):
                # A percentile check groups its examples by band.
                value[key] = {band: examples[:EXAMPLES] for band, examples in child.items()}
    elif isinstance(value, list):
        for child in value:
            trim(child)
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
    cursor.execute(f"SELECT * FROM {table} WHERE {CONDITIONS[table]} ORDER BY id", parameters)
    return [column.name for column in cursor.description], cursor.fetchall()


def dump(table, columns, rows):
    yield f"--\n-- Data for Name: {table}; Type: TABLE DATA; Schema: public; Owner: -\n--\n\n"
    yield f"COPY public.{table} ({', '.join(columns)}) FROM stdin;\n"
    for row in rows:
        yield "\t".join(literal(value) for value in row) + "\n"
    yield "\\.\n\n\n"

    # A row inserted into the loaded database must not collide with a copied row.
    last = max((row[columns.index("id")] for row in rows), default=0)
    yield f"--\n-- Name: {table}_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -\n--\n\n"
    yield f"SELECT pg_catalog.setval('public.{table}_id_seq', {last or 1}, {'true' if last else 'false'});\n\n\n"


def main():
    url = os.environ["PELICAN_BACKEND_DATABASE_URL"]

    stdout = subprocess.run(
        # btree_gin is the only extension the schema needs: a report's index spans a text column and a JSON column.
        ["pg_dump", "--schema-only", "--no-owner", "--no-privileges", "--extension=btree_gin", url],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    schema, marker, _ = stdout.partition(SCHEMA_END)
    if not marker:
        sys.exit("pg_dump wrote an unexpected ending")
    # The token in the \restrict command that guards the rest of the file is random, and would otherwise change the
    # fixture on every rebuild. Its \unrestrict command follows the ending, and is dropped with it.
    schema = re.sub(r"\\restrict \S+\n\n", "", schema)

    with psycopg.connect(url) as connection, connection.cursor() as cursor:
        # The example arrays are trimmed before the data items are chosen, so that only the surviving examples count.
        trimmed = {table: select(cursor, table, datasets=DATASETS) for table in EXAMPLE_TABLES}

        item_ids = set()
        for columns, rows in trimmed.values():
            index = columns.index("data" if "data" in columns else "meta")
            for row in rows:
                add_data_item_ids(trim(row[index]), item_ids)

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

        text = [schema]
        for table in CONDITIONS:
            columns, rows = (
                trimmed[table]
                if table in trimmed
                else select(cursor, table, datasets=DATASETS, items=items, checked=checked)
            )
            text.extend(dump(table, columns, rows))
        text.append(SCHEMA_END)

    OUT.write_bytes(gzip.compress("".join(text).encode(), compresslevel=9, mtime=0))

    print(f"{OUT}: {OUT.stat().st_size:,} bytes, {len(items):,} data items, {len(checked):,} checked")  # noqa: T201


if __name__ == "__main__":
    main()
