Refresh the fixtures
====================

``tests/fixtures/pelican-backend.sql.gz`` is the database to develop against, and ``tests/fixtures/reports.json`` is the set of responses that ``tests/api/test_serializers.py`` hands to the serializers that describe them. Both are built by scripts, from a Pelican backend database and from the dump, respectively.

Refresh them when Pelican backend changes what it writes, or when a check is added, removed or renamed.

Rebuild
-------

#. Point ``PELICAN_BACKEND_DATABASE_URL`` at the database to copy from, as in :doc:`compare-to-production`.
#. Rebuild the dump. ``pg_dump`` must be at least the server's version.

   .. code-block:: bash

      uv run --env-file .env python tests/fixtures/build_dump.py

#. Rebuild the reports, which reads the dump only:

   .. code-block:: bash

      uv run python tests/fixtures/build_reports.py

#. Load the dump, and check the pages that the new datasets serve (see :doc:`compare-to-production`).

What the dump contains
----------------------

``DATASETS`` in ``build_dump.py`` names the datasets, and the comment above it says what each one covers. Between them, they exercise every page: the time-based checks that only a dataset with an ancestor has, all six dataset-level check types, a code chart with more values than it draws bars for, a filtered dataset and its parent, a dataset whose collection metadata is null, and one that stopped before its reports were written, which is the only state in which a page can be missing its report.

The rows are copied as they are, with no scrubbing. A report is an aggregate of the data items it is about, so replacing a publisher's name or an OCID would decouple the two: the check results, charts and examples would no longer follow from the data on display. Choose datasets whose publishers publish openly.

The file is kept small by copying only a part of each dataset:

-  Every example array is cut to ``EXAMPLES`` entries.
-  The only data items copied are the ones the surviving examples point to, so that every example can be previewed.
-  ``field_level_check`` and ``resource_level_check`` hold every check of one data item, at about 90 kB each. Only the failure downloads read them, so they are copied for the lowest ``CHECKED`` data items of each dataset. The downloads therefore list fewer OCIDs than the reports count.
-  ``exchange_rates`` is emptied. Nothing in the frontend reads it.

A report's counts are over the whole dataset, and are left alone, so they exceed the number of data items copied.

After a rebuild
---------------

A declaration is only as good as its evidence, so check the ones that exist because a fixture shows a shape:

#. If the dump no longer shows a shape that a serializer allows, tighten the declaration, and delete the ``reports.json`` entry that covered it. If it shows a new one, do the reverse. Keep a declaration that only Pelican backend's code justifies, and say so in a comment.
#. Regenerate the OpenAPI document and the frontend's types, if any declaration changed (see :ref:`api-documentation`).
#. Compare the check names in ``frontend/src/config.ts`` with the new dump's, since a check that neither the config nor the fixture has is invisible until production runs it.
