Django backend
==============

The Django project is made up of two apps:

-  ``api``: Serves API requests
-  ``exporter``: Generates the exports to Google Docs

To view the API's documentation, :ref:`run the server<development>` and open http://127.0.0.1:8000/swagger-ui/.

The API is used by the Vue frontend (see the endpoints in ``frontend/src/config.js``) and for managing datasets in Pelican backend (see ``PELICAN_FRONTEND_URL`` in the `Data Registry <https://github.com/open-contracting/data-registry>`__).

.. toctree::
   :caption: Contents
   :maxdepth: 2

   settings
   integration
