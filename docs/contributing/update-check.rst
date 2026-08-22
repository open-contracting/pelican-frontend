Update a check
==============

If a major change is made to a check in Pelican backend, its ``version`` is expected to be updated.

Pelican frontend should then be updated to support *all* versions of the check, to be able to render both new and old reports. (Pelican frontend does not pre-emptively disallow new versions, since breaking changes to Pelican backend are avoided.) For example, changing the histogram bins (buckets) in Pelican backend would require supporting more bins in:

-  ``exporter/leaf_tags/dataset.py``
-  ``frontend/src/components/FrequencyChart.vue``

If you reword a check's name or description in ``frontend/src/messages/en.json``, update ``frontend/src/messages/es.json``. See :doc:`translate`. To find missed updates:

.. code-block:: bash

   git log -p frontend/src/messages/en.json
