Read a report
=============

The reports are self-documenting, with explanations in paragraphs and tooltips.

Check metadata is displayed verbatim. In principle, any useful metadata should be rendered elsewhere (`#34 <https://github.com/open-contracting/pelican-frontend/issues/34>`__, `#49 <https://github.com/open-contracting/pelican-frontend/issues/49>`__, `#50 <https://github.com/open-contracting/pelican-frontend/issues/50>`__. That said, here are the semantics of the members:

.. See docstring for complete_result_resource() and compiled-release.rst in pelican-backend.

Common members
--------------

result
  Whether the check passes.

  ``true``
    Passed
  ``false``
    Failed
  ``null``
    Not applicable
reason
  The reason the check failed or wasn't applied.
meta
  Any additional data to help interpret the result.
version
  The version of the check. If developers change a check's behavior, they increment its version.

Field-level checks
------------------

name
  The machine name of the field-level check.
value
  The field's value, if the check failed.

Compiled release-level checks
-----------------------------

application_count
  The number of times the check was applied (for example, once per array entry).
pass_count
  The number of times the check passed.
meta
  Any additional data to help interpret the result.

  failed_paths
    The failed paths if the check failed.
