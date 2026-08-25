Manage access
=============

A proxy must authenticate every request, with credentials per person, and must forward the username to Django, which signs the user in and creates their account if it doesn't exist. There is no sign-out: the browser holds the credentials.

Visibility
----------

Reports
~~~~~~~

Staff members see every report. Non-staff see only reports in their publishers' namespaces.

A publisher's namespace is its spider's name in `Kingfisher Collect <https://kingfisher-collect.readthedocs.io/en/latest/>`__, followed by a date, like ``chile_compra_bulk_2026-01-01``. Pelican backend copies a report's name into any report filtered from it, so a filtered report is in the same namespace as its parent.

Exports
~~~~~~~

An export's status is visible only to its initiating user. Google Drive manages access to exported documents.

Add a publisher
---------------

.. note::

   A publisher's users see every report in its namespace, including reports run before the publisher was added.

#. Open the `administration site <https://pelican.open-contracting.org/admin/>`__.
#. Add a publisher, entering its spider's name in Kingfisher Collect.

Add a user
----------

#. Add their credentials to the proxy (e.g. see the `deploy documentation <https://ocdsdeploy.readthedocs.io/en/latest/use/pelican.html>`__).
#. Open the `administration site <https://pelican.open-contracting.org/admin/>`__.
#. Add a user, with *Password-based authentication* disabled.
#. Add the user to their publishers.

A signed-in user with no associated publishers sees an empty homepage.

Add a staff member
------------------

A staff member sees every report, creates and deletes reports, and exports to ``GOOGLE_DRIVE_FOLDER``. Only a staff member reaches the administration site.

After adding their credentials to the proxy, run:

.. code-block:: bash

   ./manage.py createuser --staff USERNAME

Or, if the person already has an account, check *Staff status* in the administration site.
