Changelog
=========

This changelog only notes major changes, to notify other developers.

2023-01-26
----------

-  Exported reports

   -  feat: Set default templates to those used in practice. (``template`` arguments should no longer be necessary.) :issue:`32` :issue:`114`
   -  fix: Correct value distribution plot in exported documents. :issue:`85`
   -  fix: Provide clearer error messages. :issue:`31`
   -  refactor: Rewrite the tag system. :commit:`dbd97ed` :issue:`102`

-  Web reports

   -  fix: Remove pass/fail badges from checks that don't pass/fail. :issue:`7`
   -  fix: Use correct color for field-level check failures. :issue:`33`
   -  fix: Make all zeroes gray on compiled release-level checks page. :issue:`38`
   -  fix: Clarify the description of value distribution checks and of compiled release-level average scores. :issue:`42` :issue:`41`
   -  fix: Strip whitespace from user input to mitigate copy-paste errors. :issue:`28`
   -  fix: Use hyperlinks instead of JavaScript on reports list to allow native browser behavior. :issue:`35`
   -  fix: Remove context menu override to allow native browser behavior. :commit:`23428f1`
   -  fix: Remove contract value and release date visualizations from overview page. :issue:`55`
   -  fix: Correct sorting and display of reports list in edge cases. :commit:`b808827`
   -  fix: Correct spacing of page elements. :issue:`106`

-  docs: Add documentation about exporting reports and contributing code. :issue:`25` :issue:`109` :issue:`116`
-  refactor: Rewrite the API endpoints. :issue:`74` :issue:`77` :issue:`108` :issue:`13` :issue:`103`

2021-11-09
----------

-  fix: Return ``{}`` if no dataset is found by name, instead of raising ``ObjectDoesNotExist``. :commit:`49f39ac`
-  refactor: Rewrite the API endpoints for managing datasets in Pelican backend. :commit:`0481513` :commit:`6ecab3d` :commit:`49f39ac` :commit:`62ece02` :commit:`289c98a`

   -  Request:

      .. list-table::
         :header-rows: 1

         * - Before
           - After
         * - ``POST api/dataset_start``
           - ``POST api/datasets/``
         * - ``POST api/create_dataset_filter``
           - ``POST api/datasets/{id}/filter/``
         * - ``POST api/dataset_id``
           - ``GET api/datasets/find_by_name/``
         * - ``POST api/dataset_wipe``
           - ``DELETE api/datasets/{id}/``
         * - ``GET api/dataset_status/{id}``
           - ``GET api/datasets/{id}/status/``
         * - ``GET api/dataset_availability/{id}``
           - ``GET api/datasets/{id}/coverage/``
         * - ``GET api/dataset_metadata/{id}``
           - ``GET api/datasets/{id}/metadata/``

   -  Status code:

      -  Return a HTTP 2xx code, instead of ``"status": "ok"`` in the JSON response.
      -  Return HTTP 202 Accepted for creating and deleting datasets asynchronously.
      -  Return HTTP 400 Bad Request for missing request parameters when creating datasets.
      -  Return HTTP 404 Not Found, instead of raising ``ObjectDoesNotExist``.
      -  Return HTTP 404 Not Found on status action for missing dataset, instead of returning ``{}``.
      -  Return HTTP 405 Method Not Allowed for incorrect HTTP methods, instead of HTTP 200 with a JSON error message.

   -  Response body:

      -  Return a JSON object from all endpoints, instead of sometimes null (``datasets/{id}/status/``), a number (``datasets/find_by_name/``) or a string (``datasets/{id}/filter/``).
      -  Return the data as the root object, instead of under a ``"data"`` key.

2021-11-08
----------

-  refactor: Split Django applications from Django project. :commit:`df4b678` :commit:`fe94f41` :commit:`f01bcaf`
-  refactor: Move static assets out of code directory. :commit:`80bbd09`

2021-11-01
----------

-  refactor: Use `template <https://ocp-software-handbook.readthedocs.io/en/latest/python/django.html#settings>`__ for ``settings.py``. :commit:`cbacaba`

2021-10-23
----------

-  chore: Update ``models.py`` to match Pelican backend's database. :commit:`0c7448e`
