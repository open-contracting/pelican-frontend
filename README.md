# Pelican frontend

Pelican frontend has a Django backend that provides an API to the data in [Pelican backend](https://github.com/open-contracting/pelican-backend), and a Vue frontend that reports results to users.

## Getting started

Set up the git pre-commit hook:

```bash
pre-commit install
```

[Developer documentation](https://docs.google.com/document/d/1cfunGPyP-QLHOeQT3olFEHJh0J_aieUJZzxirT7Y8wk/edit)

## Django

### Getting started

Install development dependencies:

```bash
pip install pip-tools
pip-sync requirements_dev.txt
```

Run database migrations:

```bash
python backend/manage.py migrate
```

### Environment variables

See [OCP's approach to Django settings](https://ocp-software-handbook.readthedocs.io/en/latest/python/django.html#settings). New variables are:

-   `PELICAN_BACKEND_DATABASE_URL`: The [connection string](https://github.com/kennethreitz/dj-database-url#url-schema) for Pelican backend's database
-   `CORS_ALLOWED_ORIGINS`: The [origins](https://github.com/adamchainz/django-cors-headers#cors_allowed_origins-sequencestr) that are authorized to make cross-site HTTP requests
-   `TOKEN_PATH`: The path to a [Google `credentials.json` file](https://developers.google.com/workspace/guides/create-credentials)
-   `RABBIT_URL`: The [connection string](https://pika.readthedocs.io/en/stable/examples/using_urlparameters.html#using-urlparameters) for RabbitMQ
-   `RABBIT_EXCHANGE_NAME`: The name of the RabbitMQ exchange. Follow the pattern `pelican_{service}_{environment}` like `pelican_data_registry_production`
-   `DEFAULT_BASE_TEMPLATE`: The Google Docs ID for the base template
-   `DEFAULT_FIELD_TEMPLATE`: The Google Docs ID for the field-level template
-   `DEFAULT_RESOURCE_TEMPLATE`: The Google Docs ID for the resource-level template
-   `DEFAULT_DATASET_TEMPLATE`: The Google Docs ID for the dataset-level template
-   `DEFAULT_ERROR_TEMPLATE`: The Google Docs ID for the error template

### Develop

#### Pelican backend integration

Pelican backend's database is treated as a [legacy database](https://docs.djangoproject.com/en/3.2/howto/legacy-databases/), with `managed = False` in all model's `Meta` class, and with a `DATABASE_ROUTERS` setting that routes queries to its database.

To update `backend/dqt/models.py` following changes to Pelican backend's database schema:

-   Run `python backend/manage.py inspectdb > backend/dqt/models.py`
-   Replace comments at top of file
-   Replace `models.DO_NOTHING` with `on_delete=models.CASCADE`
-   `Dataset`: Add methods
-   `DatasetFilter.dataset_id_original`: Rename to `dataset_original`, add `related_name="dataset_filter_parent"`
-   `DatasetFilter.dataset_id_filtered`: Rename to `dataset_filtered`, add `related_name="dataset_filter_child"`
-   `ProgressMonitorDataset.dataset`: Add `related_name="progress"`
-   `ProgressMonitorItem.item`: Rename to `data_item`
-   `Report.type`: Change `TextField` to `CharField`, add `max_length=255`, and remove `# This field type is a guess.`

## Vue

All commands must be run from the `frontend/` directory.

### Getting started

Install dependencies:

```bash
npm install
```

### Develop

Start a development server:

```bash
npm run serve
```

Prepare a production build:

```bash
npm run build
```

This automatically sets the `NODE_ENV` environment variable to `"production"`. To [override this default](https://cli.vuejs.org/guide/mode-and-env.html), use:

```bash
npm run build -- --mode development
```

### Test

Run tests:

```bash
npm run test
```

Run linters:

```bash
npm run lint
```
