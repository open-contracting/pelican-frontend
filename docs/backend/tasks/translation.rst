Update translations
===================

Extract messages and update catalogs:

.. code-block:: bash

   python manage.py makemessages -a

Push to Transifex:

.. code-block:: bash

   tx push -s

Pull from Transifex, when ready:

.. code-block:: bash

   tx pull -f -a

Reference
---------

The ``.tx/config`` file was generated with:

.. code-block:: bash

   tx config mapping -r pelican-1.django -f dqt/locale/en/LC_MESSAGES/django.po -s en_US -t PO 'dqt/locale/<lang>/LC_MESSAGES/django.po'
