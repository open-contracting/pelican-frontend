Add a check
===========

Metadata
--------

#. Update the template in ``frontend/src/views/Overview.vue``.
#. Add new keys to ``overview`` in ``frontend/src/messages/en.js``.
#. Update the tags tuple and return value in ``backend/exporter/template_tags/overview.py``.

Field-level
-----------

#. Add new keys to ``fieldDetail.coverage`` and/or ``fieldDetail.quality`` in ``frontend/src/messages/en.js``.

The UI otherwise automatically supports new field-level checks.

Compiled release-level
----------------------

#. If a section other than ``coherent``, ``consistent`` or ``reference`` is used, add it to ``sections`` in ``frontend/src/views/Resource.vue``.
#. Add new keys to ``resourceLevel.coherent``, ``resourceLevel.consistent`` and/or ``resourceLevel.reference`` in ``frontend/src/messages/en.js``.

The UI otherwise automatically supports new compiled release-level checks.

Dataset-level
-------------

#. Add new keys to ``datasetLevel`` in ``frontend/src/messages/en.js``.
#. Update ``frontend/src/components/DatasetLevelSection.vue`` and register the check.
#. Register the check in ``frontend/src/plugins/datasetMixins.js``.

Time-based
----------

#. Add new keys to ``timeLevel`` in ``frontend/src/messages/en.js``.

The UI otherwise automatically supports new time-based checks.
