Internationalization (i18n)
===========================

Source messages (``en.json``)
-----------------------------

If two keys would hold the same text, prefer one key that serves both contexts. In such cases, prefer a noun to an adjective, because a translation might have to agree an adjective with a different subject in each context.

Write ``{'$'}`` for a dollar sign, which vue-i18n otherwise interprets.

Spanish translation (``es.json``)
---------------------------------

Terms
~~~~~

We ensure that key terms are translated consistently by referring to the `OCDS Glossary <https://docs.google.com/spreadsheets/d/171VRailLhqC3Pmw3Qkh4lIgUkmtSa7t4H2h7yntSZg8/edit?gid=1728079542#gid=1728079542>`__ and the standard's `Spanish translations <https://github.com/open-contracting/standard/tree/latest/docs/locale/es/LC_MESSAGES>`__, plus:

collection
  colección. All compiled releases from one source at one point in time, which is what a dataset-level check operates on.
dataset
  conjunto de datos. What Pelican processes, and what filtering a dataset produces. Keep it distinct from a collection: the interface shows both.
check
  comprobación. A named rule that Pelican applies to a dataset, like "Award reference" or "Monetary values are realistic".
test
  prueba. One application of a check. The interface counts both: ``resourceLevel.count_header`` counts the compiled releases to which a check was applied, and ``resourceLevel.application_count_header`` counts the individual tests performed.
coverage
  cobertura
quality
  calidad
field path
  ruta del campo
pass, fail
  A result is a noun, *éxito* or *fallo*. The action is a verb, *pasar* or *fallar*: *la prueba pasa*, *no pasan ni fallan*. An adjective is fine where the noun it agrees with is alongside it: *Ejemplos exitosos*, *Solo cobertura fallida*.

Wording
~~~~~~~

Reuse ``es.json``'s patterns for recurring sentences:

The test is skipped if…
  La prueba se omite si…
The test passes if…
  La prueba pasa si…
Since the test operates on all X objects, the test silently ignores…
  Dado que la prueba opera en todos los objetos de X, ignora silenciosamente…
Failure indicates…
  El fallo indica…
Visualizes the distribution of X values.
  Visualiza la distribución de los valores de X.
Lists the 5 most frequent pairs of…
  Lista los 5 pares más frecuentes de…
after conversion to USD if necessary
  después de la conversión a USD si es necesario

Punctuation
~~~~~~~~~~~

Write decimals with a comma: 0,1%, not 0.1%.
