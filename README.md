# Pelican frontend

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

```bash
python backend/manage.py migrate
```

### Pelican backend integration

Pelican backend's database is treated as a [legacy database](https://docs.djangoproject.com/en/3.2/howto/legacy-databases/), with `managed = False` in all model's `Meta` class, and with a `DATABASE_ROUTERS` setting that routes queries to its database.

To create `backend/dqt/models.py`:

-   Run `python backend/manage.py inspectdb > backend/dqt/models.py`
-   Remove comments at top of file
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

### Test

Run tests:

```bash
npm run test
```

Run linters:

```bash
npm run lint
```
