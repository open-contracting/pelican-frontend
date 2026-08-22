.. _i18n:

Internationalization (i18n)
===========================

``frontend/src/messages/en.json`` is the message catalog, and ``es.json`` is its Spanish translation.

Neither the frontend nor the exporter requires a translation to be complete: both fall back to English for a message it omits.

If two keys would hold the same text, prefer one key that serves both places. Where one key does, prefer a noun to an adjective: a translation might have to agree an adjective with a different subject in each place.

Write ``{'$'}`` for a dollar sign, which vue-i18n otherwise interprets.

Spanish translation
-------------------

Pelican's prose reuses the same nouns across hundreds of messages, so a term has to be settled once and then applied. Two sources settle a term:

#. The `OCDS Glossary <https://docs.google.com/spreadsheets/d/171VRailLhqC3Pmw3Qkh4lIgUkmtSa7t4H2h7yntSZg8/edit?gid=1728079542#gid=1728079542>`__, for the contracting nouns.
#. The `standard's Spanish catalogs <https://github.com/open-contracting/standard/tree/latest/docs/locale/es/LC_MESSAGES>`__, for anything OCDS names.

The terms below are the ones neither source names.

Terms
~~~~~

collection
  colección. All compiled releases from one source at one point in time, which is what a dataset-level check operates on. Not *recopilación* or *recolección*, which name the act of collecting rather than its result.
dataset
  conjunto de datos. What Pelican processes, and what a filter derives another of. Keep it distinct from a collection: the interface shows both.
check
  comprobación. The named thing a reader selects and reads a description of. Not *verificación* or *revisión*.
test
  prueba. One application of a check. The interface counts both: ``resourceLevel.count_header`` counts the compiled releases a check was applied to, and ``resourceLevel.application_count_header`` counts the individual tests run over them.
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

Reuse ``es.json``'s rendering of a recurring sentence:

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
