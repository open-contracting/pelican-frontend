Contributing
============

.. toctree::
   :caption: Contents
   :maxdepth: 1

   add-metadata
   add-check
   update-check
   compare-to-production

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

The defaults name local databases, so no configuration is needed to work against a local Pelican backend. To point a setting elsewhere, as :doc:`compare-to-production` does, copy ``.env.example`` to ``.env`` and fill in what differs. Git ignores ``.env``. Pass it to the commands that need it, rather than exporting its variables into a shell:

.. code-block:: bash

   uv run --env-file .env manage.py runserver

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

   pnpm install

.. _development:

Development
-----------

In one terminal, start the backend server:

.. code-block:: bash

   ./manage.py runserver

In another terminal, start the frontend server:

.. code-block:: bash

   cd frontend
   pnpm exec vite

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

`Pelican backend <https://pelican-backend.readthedocs.io/en/latest/>`__'s database is treated as a read-only `legacy database <https://docs.djangoproject.com/en/stable/howto/legacy-databases/>`__, with ``managed = False`` in all model's ``Meta`` class, and with a ``DATABASE_ROUTERS`` setting that routes queries to its database.

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

Frontend
~~~~~~~~

Use ``$t`` in templates and ``useI18n()`` in ``<script setup>``. `vue-i18n documents both <https://vue-i18n.intlify.dev/guide/advanced/composition.html>`__.

Likewise, use ``$emit`` in templates, and assign ``defineEmits()`` only to emit from ``<script setup>``:

.. code-block:: vue

   <!-- Yes -->
   <div @click.stop="$emit('asc')" />

   <!-- No -->
   <div @click.stop="emit('asc')" />

Emit events instead of accepting callbacks as props:

.. code-block:: vue

   <!-- Yes -->
   <SearchInput @search="ui.datasetSearch = $event" />

   <!-- No -->
   <SearchInput :on-update="search => (ui.datasetSearch = search)" />

Pass a function as a prop only as data, never as an event callback. The ``filter`` predicates are the only such props: a component applies one to its rows, rather than calling it to notify its parent.

Access template refs with `useTemplateRef() <https://vuejs.org/api/composition-api-helpers#usetemplateref>`__, not by declaring a ``ref()`` whose name matches the attribute:

.. code-block:: javascript

   // Yes
   const bar = useTemplateRef("bar");

   // No
   const bar = ref(null);

Styles
^^^^^^

Write styles in a ``<style scoped>`` block. A scoped style reaches the component's own markup and the root element of a component it renders, which covers most cases:

.. code-block:: vue

   <template>
     <BCol class="right-align" />
   </template>

   <style scoped lang="scss">
   .right-align {
       text-align: right;
   }
   </style>

Leave a block unscoped only to reach markup that the component does not render, like a third-party component's internals:

.. code-block:: scss

   // vue-multiselect renders this, so a scoped style would not match it.
   .multiselect__option--highlight {
       outline: none;
   }

Write a rule once, in ``src/scss/main.scss``, if more than one component uses the class. Element selectors belong there, too, being global wherever they are written:

.. code-block:: scss

   // Yes, in main.scss
   .collection_header { ... }

   // No, in each component that uses it, where whichever loads last wins
   .collection_header { ... }

Do not rely on the order in which stylesheets load, which is the bundler's business. To override Bootstrap, write a more specific selector, rather than an equally specific one:

.. code-block:: scss

   // Yes
   .preview .vjs-tree {
       font-size: 13px;
   }

   // No
   .vjs-tree {
       font-size: 13px;
   }

Learning
~~~~~~~~

-  `Vue <https://vuejs.org>`__
-  `Vue Router <https://router.vuejs.org>`__

Testing
-------

.. code-block:: bash

   ./manage.py test

Production
----------

.. code-block:: bash

   pnpm exec vite build
