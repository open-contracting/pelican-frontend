Update a check
==============

If a major change is made to a check in Pelican backend, its ``version`` is expected to be updated.

Pelican frontend should then be updated to support all versions of the check, to be able to render both new and old reports.

Pelican frontend does not pre-emptively disallow new versions, since breaking changes to Pelican backend are avoided.
