Environment variables
=====================

See `OCP's approach to Django settings <https://ocp-software-handbook.readthedocs.io/en/latest/python/django.html#settings>`__. New variables are:

PELICAN_BACKEND_DATABASE_URL
  The `connection string <https://github.com/kennethreitz/dj-database-url#url-schema>`__ for Pelican backend's database
CORS_ALLOWED_ORIGINS
  The `origins <https://github.com/adamchainz/django-cors-headers#cors_allowed_origins-sequencestr>`__ that are authorized to make cross-site HTTP requests
TOKEN_PATH
  The path to a `Google credentials.json file <https://developers.google.com/workspace/guides/create-credentials>`__
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
