Contributing
============

.. toctree::
   :caption: Contents
   :maxdepth: 1

   backend
   add-metadata
   add-check
   update-check

Setup
-----

Create a Python 3.8 virtual environment.

Set up the git pre-commit hook:

.. code-block:: bash

   pip install pre-commit
   pre-commit install

Backend
~~~~~~~

Change to the ``backend`` directory:

.. code-block:: bash

   cd backend

Install development dependencies:

.. code-block:: bash

   pip install pip-tools
   pip-sync requirements_dev.txt

Run database migrations:

.. code-block:: bash

   ./manage.py migrate

If you don't have an instance of `Pelican backend <https://pelican-backend.readthedocs.io/en/latest/>`__, create its database and load fixtures:

.. code-block:: bash

   createdb pelican_backend
   gunzip -c backend/tests/fixtures/pelican-backend.sql | psql pelican_backend

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

   cd backend
   ./manage.py runserver

In another terminal, start the frontend server:

.. code-block:: bash

   cd frontend
   npx vue-cli-service serve

Reference
~~~~~~~~~

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
