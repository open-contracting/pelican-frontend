Contributing
============

.. toctree::
   :caption: Contents
   :maxdepth: 1

   add-metadata
   add-check
   update-check

Setup
-----

Create a Python 3.11 virtual environment.

Set up the git pre-commit hook:

.. code-block:: bash

   pip install pre-commit
   pre-commit install

Backend
~~~~~~~

Install development dependencies:

.. code-block:: bash

   pip install -r requirements_dev.txt

Run database migrations:

.. code-block:: bash

   ./manage.py migrate

If you don't have an instance of `Pelican backend <https://pelican-backend.readthedocs.io/en/latest/>`__, create its database and load fixtures:

.. code-block:: bash

   createdb pelican_backend
   gunzip -c tests/fixtures/pelican-backend.sql | psql pelican_backend

Frontend
~~~~~~~~

Change to the ``frontend`` directory:

.. code-block:: bash

   cd frontend

Install development dependencies:

.. code-block:: bash

   npm install

.. _development:

Development
-----------

In one terminal, start the backend server:

.. code-block:: bash

   ./manage.py runserver

In another terminal, start the frontend server:

.. code-block:: bash

   cd frontend
   npx vue-cli-service serve

Backend
~~~~~~~

The Django project is made up of two apps:

-  ``api``: Serves API requests
-  ``exporter``: Generates the exports to Google Docs

API documentation
^^^^^^^^^^^^^^^^^

.. seealso::

   :ref:`api`

If you edit ``views.py``, regenerate the OpenAPI document by running the server and:

.. code-block:: bash

   curl http://127.0.0.1:8000/api/schema/ -o docs/_static/openapi.yaml

Pelican backend integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Pelican backend <https://pelican-backend.readthedocs.io/en/latest/>`__'s database is treated as a read-only `legacy database <https://docs.djangoproject.com/en/4.2/howto/legacy-databases/>`__, with ``managed = False`` in all model's ``Meta`` class, and with a ``DATABASE_ROUTERS`` setting that routes queries to its database.

To update ``api/models.py`` following changes to Pelican backend's database schema:

-  Run ``python manage.py inspectdb > api/models.py``
-  Replace comments at top of file
-  Replace ``models.DO_NOTHING`` with ``on_delete=models.CASCADE``
-  ``Dataset.meta``: Add ``blank=True, default=dict``
-  ``DatasetFilter.dataset_id_original``: Rename to ``parent``, add ``related_name="children"``
-  ``DatasetFilter.dataset_id_filtered``: Rename to ``dataset``, add ``related_name="filtered"``
-  ``ProgressMonitorDataset.dataset``: Add ``related_name="progress"``
-  ``ProgressMonitorItem.item``: Rename to ``data_item``
-  ``Report.type``: Change ``TextField`` to ``CharField``, add ``max_length=255``, and remove ``# This field type is a guess.``

Learning
~~~~~~~~

-  `Vue v2 <https://v2.vuejs.org>`__
-  `Vue CLI <https://cli.vuejs.org>`__
-  `Vue Router <https://v3.router.vuejs.org>`__

Testing
-------

Backend
~~~~~~~

.. code-block:: bash

   ./manage.py test

Frontend
~~~~~~~~

.. code-block:: bash

   npm run test

Run linters:

.. code-block:: bash

   npx vue-cli-service lint

Production
----------

Prepare a production build:

.. code-block:: bash

   npx vue-cli-service build

This sets the ``NODE_ENV`` environment variable to ``"production"``. To `override this default <https://cli.vuejs.org/guide/mode-and-env.html>`__, use:

.. code-block:: bash

   npx vue-cli-service build --mode development
