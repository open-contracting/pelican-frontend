Technical overview
==================

The Django project is made up of two apps:

-  ``api``: Serves API requests
-  ``exporter``: Generates the exports to Google Docs

To view the API's documentation, run the server and open http://127.0.0.1:8000/swagger-ui/.

The API is used by the :doc:`../../frontend/index` (see the endpoints in ``frontend/src/config.js``) and for managing datasets in Pelican backend (see ``PELICAN_FRONTEND_URL`` in the `Data Registry <https://github.com/open-contracting/data-registry>`__).
