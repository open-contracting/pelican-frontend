Changelog
=========

This changelog only notes major changes, to notify other developers.

2021-11-09
----------

-  fix: Return ``{}`` if no dataset is found by name, instead of raising ``ObjectDoesNotExist``. :commit:`49f39ac`
-  refactor: Rewrite the API endpoints for managing datasets in Pelican backend. :commit:`0481513` :commit:`6ecab3d` :commit:`49f39ac`

   -  Requests:

      -  Use the DELETE method to delete datasets.
      -  Accept the primary key in the URL path when deleting datasets, instead of in the request body.
      -  Use the GET method for the safe operation of finding a dataset by name, instead of the POST method.

   -  Responses:

      -  Return a HTTP 2xx code, instead of ``"status": "ok"`` in the JSON response.
      -  Return HTTP 202 Accepted for creating and deleting datasets asynchronously.
      -  Return HTTP 400 Bad Request for missing request parameters when creating datasets.
      -  Return HTTP 404 Not Found, instead of raising ``ObjectDoesNotExist``.
      -  Return HTTP 404 Not Found on status action for missing dataset, instead of returning ``{}``.
      -  Return HTTP 405 Method Not Allowed for incorrect HTTP methods, instead of HTTP 200 with a JSON error message.
      -  Return a JSON object from all endpoints, instead of sometimes null, a number or a string.

2021-11-08
----------

-  refactor: Split Django applications from Django project. :commit:`df4b678` :commit:`fe94f41` :commit:`f01bcaf`
-  refactor: Move static assets out of code directory. :commit:`80bbd09`
