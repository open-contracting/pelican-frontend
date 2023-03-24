Export a report
===============

To export a report to Google Drive, click the report's document icon on the homepage.

The exported *document* is built from *templates* in Google Docs.

*Tags* are added to templates to generate content within the document.

.. note::

   The main template, sub-templates and the export folder must be shared with the
   `Service Account <https://developers.google.com/workspace/guides/create-credentials?hl=en#service-account/>`__
   pelican@pelican-289615.iam.gserviceaccount.com

Tag syntax
----------

A tag starts and ends like:

.. code-block:: none

   {% ... %}

A tag contains *tokens* delimited by spaces. For example:

.. code-block:: none

   {% field path:|ocid| template:|1We-5SJ7i8i-d0c7U8t9QRstf0EHkn5zQeVh5UfDkb2c| %}

The first token is the tag's *name* (``field``). The rest are the tag's *arguments* (``path:|ocid|``, etc.).

An argument is composed of a *name*, followed by a colon, followed by its *value* between vertical bars:

.. code-block:: none

   name:|value|

-  Each tag accepts different arguments.
-  Arguments can be provided in any order.
-  An argument can be required or optional.
-  An argument name must not be repeated.

Tag types
---------

There are two types of tags:

Template tag
  This type of tag renders a template and inserts it into the document. Each template tag has access to different sub-tags.
Leaf tag
  This type of tag renders data from Pelican backend into the document. The new content inherits the styles applied to the tag.

Tag library
-----------

base template tag
~~~~~~~~~~~~~~~~~

When exporting a report, you provide the file ID for the base template.

The ``base`` tag is not available within templates. It has the other template tags as sub-tags.

overview template tag
~~~~~~~~~~~~~~~~~~~~~

This template tag renders a template for metadata about the dataset.

.. code-block:: none

   {% overview template:|...| %}

.. list-table::
   :header-rows: 1

   * - Argument
     - Value
     - Required
     - How to determine the value
   * - ``template``
     - The Google Docs ID of the overview template
     -
     - The machine-readable path component in the Google Docs URL

The ``overview`` template tag has leaf tags as sub-tags.

lifecycleObjectCount
^^^^^^^^^^^^^^^^^^^^

Renders the number of objects for the specified contracting ``stage``.

.. code-block:: none

   {% lifecycleObjectCount stage:|tender| %}

.. list-table::
   :header-rows: 1

   * - Argument
     - Value
     - Required
   * - ``stage``
     - One of planning, tender, award, contract, implementation
     - ✔️

Simple leaf tags
^^^^^^^^^^^^^^^^

Simple tags accept no arguments.

.. list-table::
   :header-rows: 1
   :widths: 3 8

   * - Tag
     - Renders
   * - ``{% id %}``
     - the ID of the dataset
   * - ``{% ancestorId %}``
     - the ID of the dataset's ancestor (for time-based checks)
   * - ``{% publisher %}``
     - the name of the dataset's publisher
   * - ``{% ocidPrefix %}``
     - the OCID prefix of the dataset
   * - ``{% dataLicense %}``
     - the data license of the dataset
   * - ``{% totalUniqueOcids %}``
     - the number of compiled releases in the dataset
   * - ``{% lifecycleImage %}``
     - this image in a frame with the number of objects per contracting stage

       .. image:: ../backend/exporter/assets/images/lifecycle.png

Date leaf tags
^^^^^^^^^^^^^^

Renders a date in the specified date format (defaults to ``datetime``).

For example:

.. code-block:: none

   {% publishingStart mode:|datetime| %}

::

   2001-02-03 04:05:06

.. code-block:: none

   {% publishingStart mode:|date| %}

::

   2001-02-03

.. code-block:: none

   {% publishingStart mode:|time| %}

::

   04:05:06

.. list-table::
   :header-rows: 1

   * - Tag
     - Renders
   * - ``{% publishingStart mode:|date| %}``
     - the earliest ``date`` among compiled releases
   * - ``{% publishingEnd mode:|date| %}``
     - the latest ``date`` among compiled releases
   * - ``{% processingStart mode:|date| %}``
     - the time at which Pelican backend started processing
   * - ``{% processingEnd mode:|date| %}``
     - the time at which Pelican backend finished processing
   * - ``{% collectingStart mode:|date| %}``
     - the time at which Kingfisher Collect started the collection
   * - ``{% collectingEnd mode:|date| %}``
     - the time at which Kingfisher Process ended the compilation

field template tag
~~~~~~~~~~~~~~~~~~

This template tag renders a template for the specified field-level check.

.. code-block:: none

   {% field path:|tender.documents.format| template:|...| }

.. list-table::
   :header-rows: 1

   * - Argument
     - Value
     - Required
     - How to determine the value
   * - ``path``
     - The path to the field
     - ✔️
     - The value in the "field path" column of the field-level checks table
   * - ``template``
     - The Google Docs ID of the field-level check template
     -
     - The machine-readable path component in the Google Docs URL

The ``field`` template tag has leaf tags as sub-tags.

All sub-tags except ``path`` require a ``level`` argument, which must be one of:

-  ``coverage`` (unavailable for ``name`` and ``description``)
-  ``coverageSet``
-  ``coverageEmpty``
-  ``quality``

path
^^^^

Renders the path to the field, like ``tender.documents.format``.

.. code-block:: none

   {% path %}

name
^^^^

Renders the name of the test, indicated by the ``level`` argument.

For example, if a ``field`` template tag sets ``path:|tender.documents.format|``:

.. code-block:: none

   {% name level:|quality| %}

will render:

   Document format is recognized

description
^^^^^^^^^^^

Renders the description of the test, indicated by the ``level`` argument.

For example, if a ``field`` template tag sets ``path:|tender.documents.format|``:

.. code-block:: none

   {% description level:|quality| %}

will render:

   The value is a string and is either an IANA Media Type or the 'offline/print' code. (The codelist is open.)

resultBoxImage
^^^^^^^^^^^^^^

Renders a horizontal bar plot describing the pass/fail rate of the test, indicated by the ``level`` argument.

.. code-block:: none

   {% resultBoxImage level:|quality| %}

Count leaf tags
^^^^^^^^^^^^^^^

Renders the number of times the test, indicated by the ``level`` argument, ran, passed or failed.

.. list-table::
   :header-rows: 1

   * - Tag
     - Renders
   * - ``{% checkedCount level:|quality| %}``
     - the number of times the test ran
   * - ``{% passedCount level:|quality| %}``
     - the number of times the test passed
   * - ``{% failedCount level:|quality| %}``
     - the number of times the test failed

Sample leaf tags
^^^^^^^^^^^^^^^^

Renders a sample list of OCIDs that passed (or failed) the test indicated by the ``level`` argument.

.. code-block:: none

   {% passedExamples level:|quality| mode:|multipleLines| max:|5| %}

.. code-block:: none

   {% failedExamples level:|quality| mode:|multipleLines| max:|5| %}

.. list-table::
   :header-rows: 1

   * - Argument
     - Value
     - Required
   * - ``mode``
     - One of:

       oneLine
         Render a comma-separated list (default)
       multipleLines
         Render consecutive paragraphs
     -
   * - ``max``
     - The maximum sample size
     -

resource template tag
~~~~~~~~~~~~~~~~~~~~~

.. note::

   "resource" is "compiled release" in the web report.

This template tag renders a template for the specified compiled release-level check.

.. code-block:: none

   {% resource check:|coherent.dates| template:|...| }

.. list-table::
   :header-rows: 1

   * - Argument
     - Value
     - Required
     - How to determine the value
   * - ``check``
     - The name of the check
     - ✔️
     - The last part of the URL when viewing the check
   * - ``template``
     - The Google Docs ID of the compiled release-level check template
     -
     - The machine-readable path component in the Google Docs URL

The ``resource`` template tag has leaf tags as sub-tags.

Simple leaf tags
^^^^^^^^^^^^^^^^

Simple tags accept no arguments.

.. list-table::
   :header-rows: 1

   * - Tag
     - Renders
   * - ``{% name %}``
     - the name of the check
   * - ``{% description %}``
     - the description of the check
   * - ``{% checkedCount %}``
     - the number of times the test ran
   * - ``{% passedCount %}``
     - the number of times the test passed
   * - ``{% failedCount %}``
     - the number of times the test failed
   * - ``{% notAvailableCount %}``
     - the number of times the test was skipped
   * - ``{% resultBoxImage %}``
     - a horizontal bar plot describing the pass/fail/not applicable rate of the test

Sample leaf tags
^^^^^^^^^^^^^^^^

Renders a sample list of OCIDs that passed (or failed, or skipped) the test.

.. code-block:: none

   {% passedExamples mode:|multipleLines| max:|5| %}

.. code-block:: none

   {% failedExamples mode:|multipleLines| max:|5| %}

.. code-block:: none

   {% notAvailableExamples mode:|multipleLines| max:|5| %}

.. list-table::
   :header-rows: 1

   * - Argument
     - Value
     - Required
   * - ``mode``
     - One of:

       oneLine
         Render a comma-separated list (default)
       multipleLines
         Render consecutive paragraphs
     -
   * - ``max``
     - The maximum sample size
     -

dataset template tag
~~~~~~~~~~~~~~~~~~~~

.. note::

   "dataset" is "collection" in the web report.

This template tag renders a template for the specified dataset-level check.

.. code-block:: none

   {% dataset check:|distribution.tender_value| template:|...| }

.. list-table::
   :header-rows: 1

   * - Argument
     - Value
     - Required
     - How to determine the value
   * - ``check``
     - The name of the check
     - ✔️
     - The last part of the URL when viewing the check
   * - ``template``
     - The Google Docs ID of the dataset-level check template
     -
     - The machine-readable path component in the Google Docs URL

The ``dataset`` template tag has leaf tags as sub-tags.

The available tags vary, depending on the type of check.

Common simple leaf tags
^^^^^^^^^^^^^^^^^^^^^^^

Simple tags accept no arguments.

.. list-table::
   :header-rows: 1

   * - Tag
     - Renders
   * - ``{% name %}``
     - the name of the check
   * - ``{% description %}``
     - the description of the check
   * - ``{% result %}``
     - the result of the check ("Passed", "Failed" or "Undefined")
   * - ``{% value %}``
     - the value of the check (0 to 100, or "Undefined")

Code distribution checks
^^^^^^^^^^^^^^^^^^^^^^^^

share
'''''

Renders the percentage of cases in which the field equals the ``value``.

If ``value`` isn't set, renders 100%.

.. code-block:: none

   {% share value:|open| decimals:|2| %}

.. list-table::
   :header-rows: 1

   * - Argument
     - Value
     - Required
   * - ``value``
     - A code
     -
   * - ``decimals``
     - The number of decimals (default 0)
     -

count
'''''

Renders the number of cases in which the field equals the ``value``.

If ``value`` isn't set, renders the number of occurrences of the field.

.. code-block:: none

   {% count value:|open| %}

examples
''''''''

Renders a sample list of OCIDs in which the field equals the ``value``.

If ``value`` isn't set, renders a sample list of OCIDs in which the field occurs.

.. code-block:: none

   {% examples value:|1| mode:|multipleLines| max:|5| %}

resultBoxImage
''''''''''''''

Renders a horizontal bar plot describing the number of occurrences of each field value.

.. code-block:: none

   {% resultBoxImage %}

Value distribution checks
^^^^^^^^^^^^^^^^^^^^^^^^^

share
'''''

Renders the percentage of the total value of all amounts represented by the total value of the amounts in the percentile range indicated by the ``percentageRange`` argument.

``0-1``
   (total value of the top 0-1% of amounts) / (total value of all amounts)
``1-5``
   (total value of the top 1-5% of amounts) / (total value of all amounts)
``5-20``
   (total value of the top 5-20% of amounts) / (total value of all amounts)
``20-50``
   (total value of the top 20-50% of amounts) / (total value of all amounts)
``50-100``
   (total value of the top 50-100% of amounts) / (total value of all amounts)

If ``percentageRange`` isn't set, renders 100%.

.. code-block:: none

   {% share percentageRange:|50-100| decimals:|2| %}

.. list-table::
   :header-rows: 1

   * - Argument
     - Value
     - Required
   * - ``percentageRange``
     - One of 0-1, 1-5, 5-20, 20-50, 50-100
     -
   * - ``decimals``
     - The number of decimals (default 0)
     -

count
'''''

Renders the number of amounts in the percentile range indicated by the ``percentageRange`` argument.

If ``value`` isn't set, renders the total number of amounts.

.. code-block:: none

   {% count percentageRange:|50-100| %}

examples
''''''''

.. note::

   Pelican backend stores at most 10 samples per percentile range.

Renders a sample list of OCIDs in which an amount is within the percentile range indicated by the ``percentageRange`` argument.

If ``percentageRange`` isn't set, renders a sample list of OCIDs in which an amount occurs.

.. code-block:: none

   {% examples percentageRange:|1| mode:|multipleLines| max:|5| %}

sum
'''

Renders the total value of the amounts in the percentile range indicated by the ``percentageRange`` argument.

if ``percentageRange`` isn't set, renders the total value of all amounts.

.. code-block:: none

   {% sum percentageRange:|50-100| %}

resultBoxImage
''''''''''''''

Renders a horizontal bar plot describing the number of amounts in each percentile range.

.. code-block:: none

   {% resultBoxImage %}

Value repetition checks
^^^^^^^^^^^^^^^^^^^^^^^

share
'''''

Renders the percentage of values in which the amount-currency pair at the specified ``rank`` occurs.

If ``rank`` isn't set, renders 100%.

.. code-block:: none

   {% share rank:|1| decimals:|2| %}

.. list-table::
   :header-rows: 1

   * - Argument
     - Value
     - Required
   * - ``rank``
     - One of 1, 2, 3, 4, 5
     -
   * - ``decimals``
     - The number of decimals (default 0)
     -

count
'''''

Renders the number of values in which the amount-currency pair at the specified ``rank`` occurs.

If ``rank`` isn't set, renders the number of values in which the 5 most frequent pairs occur.

.. code-block:: none

   {% count rank:|1| %}

examples
''''''''

Renders a sample list of OCIDs in which the amount-currency pair at the specified ``rank`` occurs.

If ``rank`` isn't set, renders a sample list of OCIDs in which the 5 most frequent pairs occur.

.. code-block:: none

   {% examples rank:|1| mode:|multipleLines| max:|5| %}

amount
''''''

Renders the amount-currency pair (like "10000 USD") at the specified ``rank`` (required argument).

.. code-block:: none

   {% amount rank:|1| %}

resultBoxImage
''''''''''''''

Renders a table with the 5 most frequent amount-currency pairs with the columns:

Value
  the amount and currency
Share
  the percentage of values in which the pair occurs
Occurrences
  the number of values in which the pair occurs

.. code-block:: none

   {% resultBoxImage %}

Buyer distribution check
^^^^^^^^^^^^^^^^^^^^^^^^

buyerCount
''''''''''

Renders the number of unique buyers that occur the ``countRange`` number of times.

``1``
   the number of unique buyers that occur only once
``2-20``
   the number of unique buyers that occur 2-20 times
``21-50``
   the number of unique buyers that occur 21-50 times
``51-100``
   the number of unique buyers that occur 51-100 times
``100+``
   the number of unique buyers that occur 100+ times

If ``countRange`` isn't set, renders the total number of unique buyers (same as ``{% totalBuyerCount %}``).

.. code-block:: none

   {% buyerCount countRange:|2-20| %}

ocidCount
'''''''''

Renders the number of OCIDs in which the buyer occurs the ``countRange`` number of times.

If ``countRange`` isn't set, renders the total number of OCIDs (same as ``{% totalOcidCount %}``).

.. code-block:: none

   {% ocidCount countRange:|2-20| %}

Simple leaf tags
''''''''''''''''

.. list-table::
   :header-rows: 1

   * - Tag
     - Renders
   * - ``{% totalBuyerCount %}``
     - the number of unique buyers for which the ``identifier`` is set
   * - ``{% totalOcidCount %}``
     - the number of OCIDs in which the buyer's ``identifier`` is set
   * - ``{% examples %}``
     - a sample list of OCIDs in which the buyer occurs in only that OCID

Buyer repetition check
^^^^^^^^^^^^^^^^^^^^^^

These include simple and sample leaf tags.

.. list-table::
   :header-rows: 1

   * - Tag
     - Renders
   * - ``{% buyerIdentifierId %}``
     - the most common buyer's ``.identifier.id``
   * - ``{% buyerIdentifierScheme %}``
     - the most common buyer's ``.identifier.scheme``
   * - ``{% ocidCount %}``
     - the number of OCIDs in which the most common buyer occurs
   * - ``{% ocidShare %}``
     - the percentage of OCIDs in which the most common buyer occurs
   * - ``{% totalOcidCount %}``
     - the number of OCIDs in which the buyer's ``identifier`` is set
   * - ``{% examples max:|5| %}``
     - a sample list of OCIDs in which the most common buyer occurs

Other checks
^^^^^^^^^^^^

These include simple and sample leaf tags.

.. list-table::
   :header-rows: 1

   * - Tag
     - Renders
   * - ``{% checkedCount %}``
     - the number of times the test was run
   * - ``{% passedCount %}``
     - the number of times the test passed
   * - ``{% failedCount %}``
     - the number of times the test failed
   * - ``{% resultBoxImage %}``
     - a horizontal bar plot describing the pass/fail rate of the test
   * - ``{% passedExamples max:|5| %}``
     - a sample list of OCIDs that passed the test
   * - ``{% failedExamples max:|5| %}``
     - a sample list of OCIDs that failed the test
