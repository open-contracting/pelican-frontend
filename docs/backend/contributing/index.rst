Contributing
============

Create a Python 3.8 virtual environment.

Install development dependencies:

.. code-block:: bash

   pip install pip-tools
   pip-sync requirements_dev.txt

Run database migrations:

.. code-block:: bash

   ./manage.py migrate

If you don't have an instance of `Pelican backend <https://pelican-backend.readthedocs.io/en/latest/>`__, create its database and run its migrations:

.. code-block:: bash

   createdb pelican_backend
   curl -sS \
     https://raw.githubusercontent.com/open-contracting/pelican-backend/main/pelican/migrations/001_base.sql \
     https://raw.githubusercontent.com/open-contracting/pelican-backend/main/pelican/migrations/002_constraints.sql \
     | psql pelican_backend -f -
