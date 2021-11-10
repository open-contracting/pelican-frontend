Changelog
=========

This changelog only notes major changes, to notify other developers.

2021-11-09
----------

-  fix: Return ``{}`` if no dataset is found by name, instead of raising ``ObjectDoesNotExist``.
-  refactor: Rewrite the API endpoints for managing Pelican backend.

   -  Requests:

      -  Use the DELETE method to delete datasets.
      -  Use the GET method for the safe operation of finding a dataset by name, instead of the POST method.
      -  Accept the primary key in the URL path, instead of in the request body.

   -  Responses:

      -  Return a HTTP 2xx code, instead of ``"status": "ok"`` in the JSON response.
      -  Return HTTP 202 Accepted for creating and deleting datasets asynchronously.
      -  Return HTTP 400 Bad Request for missing request parameters when creating datasets.
      -  Return HTTP 404 Not Found, instead of raising ``ObjectDoesNotExist``.
      -  Return HTTP 405 Method Not Allowed for incorrect HTTP methods, instead of HTTP 200 with a JSON error message.
      -  Return a JSON object from all endpoints, instead of sometimes null, a number or a string.

2021-11-08
----------

-  refactor: Split Django applications from Django project. :commit:`df4b678` :commit:`fe94f41` :commit:`f01bcaf`
-  refactor: Move static assets out of code directory. :commit:`80bbd09`
