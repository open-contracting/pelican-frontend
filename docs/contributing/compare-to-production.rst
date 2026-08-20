Comparing to production
=======================

`pelican.open-contracting.org <https://pelican.open-contracting.org>`__ runs ``main``. Point a local server at the same database, and dataset IDs match, so any page can be opened side by side with its production counterpart. The frontend has no automated tests, so this is the check that a branch has not regressed.

.. attention::

   Configured this way, the local backend reads the **production** database and publishes to the **production** RabbitMQ. Browsing is safe. These endpoints are not:

   -  ``DatasetViewSet.create`` (``POST datasets/``) publishes ``ocds_kingfisher_extractor_init``. No page reaches it.
   -  ``DatasetViewSet.filter`` (``POST datasets/{id}/filter/``) publishes ``dataset_filter_extractor_init``. The filter modal's **submit** button reaches it.
   -  ``DatasetViewSet.destroy`` (``DELETE datasets/{id}/``) publishes ``wiper_init``. No page reaches it.
   -  ``POST generate-report`` creates Google Docs through the service account. The report modal's **submit** button reaches it.

   Opening either modal and editing its fields is safe: ``dataset_filter_items`` is a POST, but it only reads, and exercising it is how the filter modal's watcher gets tested. Only the two submit buttons are dangerous.

Configuration
-------------

Copy ``.env.example`` to ``.env`` and fill in the connection strings and the production credentials. Git ignores ``.env``. Load it when starting the backend, rather than exporting the variables into a shell, so that the credentials stay out of shell history:

.. code-block:: bash

   uv run --env-file .env manage.py runserver

Start the frontend server as usual (see :ref:`development`). Do not use ``vite preview``: it does not proxy ``/api``, so a build served that way gets no data, and every page looks broken for the wrong reason.

Choosing datasets
-----------------

No one dataset exercises everything. Select for:

-  Time checks, without which ``/time/:id/detail/:check`` is unreachable
-  All six dataset check types
-  A mix of passing and failing checks, since threshold colouring only diverges when shares straddle ``DATASET_CHECK_TICKS``
-  Enough field and resource checks to sort and search

Query the report endpoints instead of clicking around. For example, to find the datasets that have time checks:

.. code-block:: bash

   curl -s http://localhost:8000/api/datasets/ | python3 -c "
   import json, sys, urllib.request
   for i in json.load(sys.stdin):
       with urllib.request.urlopen(f\"http://localhost:8000/api/datasets/{i['id']}/time_based_report/\", timeout=30) as r:
           if json.load(r):
               print(i['id'])
   "

Routes
------

``/``
   Dataset list, four sort columns, search

``/overview/:id``
   Metadata blocks, tooltips

``/field/:id``
   Table and tree layouts, search, filter dropdown, reset sorting

``/resource/:id``
   Three sections, expand and collapse, average scores

``/dataset/:id``
   Five sections in order, check cards, charts

``/time/:id``
   Check list

``/field/:id/detail/:path``
   Result boxes, example boxes, preview pane

``/resource/:id/detail/:check``
   Example boxes, preview pane

``/dataset/:id/detail/:check``
   One visit per check type, plus one check that could not run

``/time/:id/detail/:check``
   Example boxes, new and old row pairs

Load each route **directly**, as well as reaching it in-app. The store is cold on the first path and warm on the second, and that difference is what exposes render bugs in the detail views.

Screenshots miss interaction, so also exercise: sort buttons, the search debounce, the filter dropdowns on four pages, both modals (**without submitting**), example preview, download and copy to clipboard, tree expand and collapse, tooltips, and detail links. Close and reopen both modals, too, which is how fields turned out to persist between openings.

Gotchas
-------

-  Restart the frontend server after editing ``src/scss/_variables.scss``. Vite injects it through ``css.preprocessorOptions.scss.additionalData`` and does not track it as a dependency, so variable changes do not reach already-compiled CSS on hot reload. Component ``<style>`` blocks hot-reload normally.
-  Clipboard permissions are granted only to a headed browser, so headless testing of copy is worthless.
-  Engines disagree about the clipboard: Chromium rejects a blob whose type differs from the ``ClipboardItem``'s, and WebKit rejects ``write()`` with a ``DOMException`` rather than the underlying error. Test copy in both.
