Add a check
===========

In all cases:

#. Add a line to ``exporter/translations.py``

Field-level
-----------

#. Add new keys to ``fieldDetail.coverage`` and/or ``fieldDetail.quality`` in ``frontend/src/messages/en.js``

The UI otherwise automatically supports new field-level checks.

Compiled release-level
----------------------

#. Add an element to ``CHECKS`` in ``exporter/template_tags/resource.py``
#. Add an element to ``RESOURCE_CHECK_ORDER`` in ``frontend/src/config.js``
#. If a section other than ``coherent``, ``consistent`` or ``reference`` is used, add it to ``RESOURCE_CHECK_SECTIONS`` in ``frontend/src/config.js``
#. Add new keys to ``resourceLevel.coherent``, ``resourceLevel.consistent`` and/or ``resourceLevel.reference`` in ``frontend/src/messages/en.js``

The UI otherwise automatically supports new compiled release-level checks.

Dataset-level
-------------

#. Add a key-value pair to ``CHECK_TYPES`` in ``exporter/template_tags/dataset.py``
#. Add a key-value pair to ``DATASET_CHECK_TYPES`` in ``frontend/src/config.js``, and to ``DATASET_CHECK_TICKS`` and ``DATASET_CHECK_STYLES`` if the check type uses them
#. Add an element to the appropriate array in ``DATASET_CHECK_SECTIONS`` in ``frontend/src/config.js``
#. Add new keys to ``datasetLevel`` in ``frontend/src/messages/en.js``

The UI otherwise automatically supports new dataset-level checks, unless a new check type is needed, which requires a new branch in ``frontend/src/components/DatasetLevelCheck.vue``.

Time-based
----------

#. Add new keys to ``timeLevel`` in ``frontend/src/messages/en.js``

The UI otherwise automatically supports new time-based checks.
