Vue frontend
============

All commands must be run from the ``frontend/`` directory.

Getting started
---------------

Install dependencies:

.. code:: bash

   npm install

Develop
-------

Start a development server:

.. code:: bash

   npm run serve

Prepare a production build:

.. code:: bash

   npm run build

This automatically sets the ``NODE_ENV`` environment variable to ``"production"``. To `override this default <https://cli.vuejs.org/guide/mode-and-env.html>`__, use:

.. code:: bash

   npm run build -- --mode development

Test
----

Run tests:

.. code:: bash

   npm run test

Run linters:

.. code:: bash

   npm run lint
