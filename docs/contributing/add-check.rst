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
#. Add an element to ``order`` in ``frontend/src/components/ResourceLevelList.vue``
#. If a section other than ``coherent``, ``consistent`` or ``reference`` is used, add it to ``sections`` in ``frontend/src/views/Resource.vue``
#. Add new keys to ``resourceLevel.coherent``, ``resourceLevel.consistent`` and/or ``resourceLevel.reference`` in ``frontend/src/messages/en.js``

The UI otherwise automatically supports new compiled release-level checks.

Dataset-level
-------------

#. Add a key-value pair to ``CHECK_TYPES`` in ``exporter/template_tags/dataset.py``
#. Add a key-value pair to ``checkTypeData`` in ``frontend/src/plugins/datasetMixins.js``
#. Add an element to the appropriate array in ``frontend/src/components/DatasetLevelSection.vue``
#. Add new keys to ``datasetLevel`` in ``frontend/src/messages/en.js``

The UI otherwise automatically supports new compiled release-level checks.

Time-based
----------

#. Add new keys to ``timeLevel`` in ``frontend/src/messages/en.js``

The UI otherwise automatically supports new time-based checks.
