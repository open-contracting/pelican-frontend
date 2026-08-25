from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from api.rabbitmq import decorator

MODULE = "api.rabbitmq"
BODY = b'{"export_id": 1}'


class DecoratorTests(SimpleTestCase):
    def setUp(self):
        super().setUp()
        self.nack = self.enterContext(patch(f"{MODULE}.nack"))
        self.connection = Mock()
        self.enterContext(patch(f"{MODULE}.connections")).all.return_value = [self.connection]

    def run_decorator(self, callback):
        decorator(Mock(return_value={}), callback, Mock(), Mock(), Mock(), Mock(), BODY)

    def test_closes_connections(self):
        callback = Mock()

        self.run_decorator(callback)

        callback.assert_called_once()
        self.connection.close.assert_called_once_with()
        self.nack.assert_not_called()

    def test_discards_the_message(self):
        def callback(*args):
            raise ValueError("anything")

        with self.assertLogs(MODULE, level="ERROR") as context:
            self.run_decorator(callback)

        # The exception is passed to the logger, since the errback runs outside the exception handler.
        self.assertEqual(context.records[0].exc_info[0], ValueError)
        self.assertEqual(
            context.records[0].getMessage(), f"Unhandled exception when consuming {BODY!r}, discarding message"
        )
        self.assertEqual(self.nack.call_args.kwargs, {"requeue": False})
        self.connection.close.assert_called_once_with()
