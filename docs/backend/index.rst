Django backend
==============

All commands must be run from the ``backend/`` directory.

Getting started
---------------

Install development dependencies:

.. code:: bash

   pip install pip-tools
   pip-sync requirements_dev.txt

Run database migrations:

.. code:: bash

   ./manage.py migrate
