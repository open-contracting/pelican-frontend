Reference
=========

.. _api:

API
---

.. toctree::

   redoc
   swagger-ui

To view the API's documentation in development, :ref:`run the server<development>` and open http://127.0.0.1:8000/api/schema/swagger-ui/ or http://127.0.0.1:8000/api/schema/redoc/.

The API is used by the Vue frontend (see the endpoints in ``frontend/src/config.js``) and for managing datasets in Pelican backend (see ``PELICAN_FRONTEND_URL`` in the `Data Registry <https://ocp-data-registry.readthedocs.io/en/latest/reference/>`__).

.. _environment-variables:

Environment variables
---------------------

See `OCP's approach to Django settings <https://ocp-software-handbook.readthedocs.io/en/latest/python/django.html#settings>`__. New variables are:

PELICAN_BACKEND_DATABASE_URL
  The `connection string <https://github.com/kennethreitz/dj-database-url#url-schema>`__ for Pelican backend's database
LOG_LEVEL
  The log level of the root logger
CORS_ALLOWED_ORIGINS
  The `origins <https://github.com/adamchainz/django-cors-headers#cors_allowed_origins-sequencestr>`__ that are authorized to make cross-site HTTP requests
SERVICE_ACCOUNT_JSON_FILE
  The filename of the `service account JSON file <https://developers.google.com/workspace/guides/create-credentials#service-account>`__
RABBIT_URL
  The `connection string <https://pika.readthedocs.io/en/stable/examples/using_urlparameters.html#using-urlparameters>`__ for RabbitMQ
RABBIT_EXCHANGE_NAME
  The name of the RabbitMQ exchange. Follow the pattern ``pelican_{service}_{environment}`` like ``pelican_data_registry_production``
DEFAULT_BASE_TEMPLATE
  The Google Docs ID for the base template
DEFAULT_FIELD_TEMPLATE
  The Google Docs ID for the field-level template
DEFAULT_RESOURCE_TEMPLATE
  The Google Docs ID for the resource-level template
DEFAULT_DATASET_TEMPLATE
  The Google Docs ID for the dataset-level template
DEFAULT_ERROR_TEMPLATE
  The Google Docs ID for the error template
