Contributing
============

Create a Python 3.8 virtual environment.

Setup
-----

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

   cd backend

Install development dependencies:

.. code-block:: bash

   npm install

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
