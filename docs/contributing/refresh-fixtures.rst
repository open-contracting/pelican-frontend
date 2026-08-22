Refresh the fixtures
====================

``tests/fixtures/pelican-backend.sql.gz`` is the database to develop against, and ``tests/fixtures/reports.json`` is the set of responses that ``tests/api/test_serializers.py`` hands to the serializers that describe them. ``api/management/commands/refreshfixtures.py`` writes both, and documents which datasets it copies, why each one is there, and what it leaves out.

Refresh them when Pelican backend changes what it writes, or when a check is added, removed or renamed.

Rebuild
-------

#. Point ``PELICAN_BACKEND_DATABASE_URL`` at the database to copy from, as in :doc:`compare-to-production`.
#. Rebuild both fixtures. ``pg_dump`` must be at least the server's version.

   .. code-block:: bash

      uv run --env-file .env manage.py refreshfixtures

#. Load the dump, and check the pages that the new datasets serve (see :doc:`compare-to-production`).

After a rebuild
---------------

A declaration is only as good as its evidence, so check the ones that exist because a fixture shows a shape:

#. If the dump no longer shows a shape that a serializer allows, tighten the declaration, and delete the ``reports.json`` entry that covered it. If it shows a new one, do the reverse. Keep a declaration that only Pelican backend's code justifies, and say so in a comment.
#. Regenerate the OpenAPI document and the frontend's types, if any declaration changed (see :ref:`api-documentation`).
#. Compare the check names in ``frontend/src/config.ts`` with the new dump's, since a check that neither the config nor the fixture has is invisible until production runs it.
