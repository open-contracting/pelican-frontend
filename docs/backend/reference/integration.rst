Pelican backend integration
===========================

Pelican backend's database is treated as a read-only `legacy database <https://docs.djangoproject.com/en/3.2/howto/legacy-databases/>`__, with ``managed = False`` in all model's ``Meta`` class, and with a ``DATABASE_ROUTERS`` setting that routes queries to its database.

To update ``backend/dqt/models.py`` following changes to Pelican backend's database schema:

-  Run ``python backend/manage.py inspectdb > backend/dqt/models.py``
-  Replace comments at top of file
-  Replace ``models.DO_NOTHING`` with ``on_delete=models.CASCADE``
-  ``Dataset``: Add methods
-  ``Dataset.meta``: Add ``blank=True, default=dict``
-  ``DatasetFilter.dataset_id_original``: Rename to ``dataset_original``, add ``related_name="dataset_filter_parent"``
-  ``DatasetFilter.dataset_id_filtered``: Rename to ``dataset_filtered``, add ``related_name="dataset_filter_child"``
-  ``ProgressMonitorDataset.dataset``: Add ``related_name="progress"``
-  ``ProgressMonitorItem.item``: Rename to ``data_item``
-  ``Report.type``: Change ``TextField`` to ``CharField``, add ``max_length=255``, and remove ``# This field type is a guess.``

