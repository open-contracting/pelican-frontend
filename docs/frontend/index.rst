Vue frontend
============

This section of the documentation assumes you are in the ``frontend/`` directory.

Getting started
---------------

Install dependencies:

.. code-block:: bash

   npm install

Develop
-------

Start a development server:

.. code-block:: bash

   npm run serve

Prepare a production build:

.. code-block:: bash

   npm run build

This automatically sets the ``NODE_ENV`` environment variable to ``"production"``. To `override this default <https://cli.vuejs.org/guide/mode-and-env.html>`__, use:

.. code-block:: bash

   npm run build -- --mode development

Test
----

Run tests:

.. code-block:: bash

   npm run test

Run linters:

.. code-block:: bash

   npm run lint
