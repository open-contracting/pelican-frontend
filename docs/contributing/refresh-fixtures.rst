Refresh the fixtures
====================

``tests/fixtures/pelican-backend.sql.gz`` is a sample database to develop against, and ``tests/fixtures/reports.json`` is used to test serializers.

``api/management/commands/refreshfixtures.py`` writes both and documents which datasets it copies, why each one is there, and what it leaves out.

Refresh the fixtures when Pelican backend changes what it writes, or when a check is added, removed or renamed.

Refresh
-------

#. Copy ``.env.example`` to ``.env``, and set ``PELICAN_BACKEND_DATABASE_URL`` to the database to copy from.

   .. code-block:: bash

      cp .env.example .env

#. Refresh the fixtures. ``pg_dump`` must be at least the server's version.

   .. code-block:: bash

      uv run --env-file .env manage.py refreshfixtures

If the command warns about deleted datasets, choose replacements if possible, and refresh again.

After a refresh
---------------

#. Load the dump.
#. Check that each dataset shows what it was copied for (see :doc:`compare-to-production`):

   -  its row in the dataset picker
   -  its metadata in the dataset overview
   -  its charts in the collection page
   -  its examples in a field-level and a compiled release-level detail page
   -  its pairs in the time-based pages

#. Match the serializers to what Pelican backend writes (the fixtures being merely evidence of it):

   -  Remove a ``required=False`` or ``allow_null=True`` when neither the dump nor Pelican backend's code has that shape any more, and delete the ``reports.json`` entry that covered it.
   -  Keep a ``required=False`` or ``allow_null=True`` when only Pelican backend's code has that shape, and state the condition under which it writes it in a comment, as ``KingfisherMetadataSerializer`` does for a collection with no rows in Kingfisher Process.
   -  Add a ``required=False`` or ``allow_null=True``, and a ``reports.json`` entry, when the dump has a shape that the serializer rejects.

#. If you edit a serializer, :ref:`regenerate the OpenAPI document and the frontend's types<api-documentation>`.
#. Compare the check names in ``frontend/src/config.ts`` with those in the new dump.

   -  Configure a check that the dump has and the configuration lacks (see :doc:`add-check`).

      .. note:: A dataset-level check that no section lists is never rendered, and a compiled release-level check that ``RESOURCE_CHECK_ORDER`` omits is sorted after the rest.

   -  Remove a check name that Pelican backend no longer writes, and its messages.
