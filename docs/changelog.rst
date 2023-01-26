Changelog
=========

This changelog only notes major changes, to notify other developers.

2022-01-26
----------

-  refactor: Rewrite the tag system. :commit:`dbd97ed`

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
           - ``POST datasets/``
         * - ``POST api/create_dataset_filter``
           - ``POST datasets/{id}/filter/``
         * - ``POST api/dataset_id``
           - ``GET datasets/find_by_name/``
         * - ``POST api/dataset_wipe``
           - ``DELETE datasets/{id}/``
         * - ``GET api/dataset_status/{id}``
           - ``GET datasets/{id}/status/``
         * - ``GET api/dataset_availability/{id}``
           - ``GET datasets/{id}/coverage/``
         * - ``GET api/dataset_metadata/{id}``
           - ``GET datasets/{id}/metadata/``

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
