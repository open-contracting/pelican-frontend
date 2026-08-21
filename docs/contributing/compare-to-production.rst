Compare to production
=====================

The frontend has no automated tests (:issue:`73`). Check for regressions by comparing to production.

.. attention::

   When navigating production, do not click the submit buttons of the *Dataset filtering* and *Export report* modals. Call production's API with ``GET`` only – apart from ``POST dataset-filter-items/``, which runs a ``COUNT`` only. Locally, these are harmless, as long as no ``credentials.json`` file exists and no ``RABBIT_URL`` environment variable is set.

Setup
-----

#. Copy ``.env.example`` to ``.env`` and add your database and HTTP authentication credentials.

   .. code-block:: bash

      cp .env.example .env

#. Start the backend server:

   .. code-block:: bash

      uv run --env-file .env manage.py runserver

#. Start the frontend server (see :ref:`development`).

Choose datasets
---------------

Find a set of datasets to exercise:

-  Time checks (otherwise, ``/time/:id/detail/:check`` is unreachable)
-  All six dataset check types:

   -  ``code``
   -  ``percentile`` ("… value distribution")
   -  ``top3`` ("… value repetition")
   -  ``numeric`` ("Other" section)
   -  ``biggest_share`` ("Buyer repetition")
   -  ``single_value_share`` ("Buyer distribution")

-  A mix of passing and failing dataset-level checks
-  A mix of passing, failing and N/A compiled release-level checks
-  A mix of passing and failing field-level quality checks

Gotchas
-------

-  A route loaded directly has a cold store, and a route reached in-app has a warm store. The detail views can render differently in each case, so try both.
-  After editing ``src/scss/_variables.scss``, you need to restart the frontend server.
-  If testing the *Copy to clipboard* feature, test it in both Chromium and WebKit, which behave differently: Chromium rejects a ``Blob`` whose type differs from the ``ClipboardItem``'s, and WebKit rejects ``write()`` with a ``DOMException`` rather than the underlying error.
