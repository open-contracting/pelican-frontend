Django backend
==============

All commands must be run from the ``backend/`` directory.

.. toctree::
   :maxdepth: 2

   tasks/index
   reference

Getting started
---------------

Install development dependencies:

.. code:: bash

   pip install pip-tools
   pip-sync requirements_dev.txt

Run database migrations:

.. code:: bash

   ./manage.py migrate
