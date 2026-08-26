from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from api.rabbitmq import close_old_connections_and_discard

BODY = b'{"export_id": 1}'


class DecoratorTests(SimpleTestCase):
    def setUp(self):
        super().setUp()
        self.nack = self.enterContext(patch("yapw.decorators.nack"))
        self.connection = Mock()
        self.enterContext(patch("django.db.connections")).all.return_value = [self.connection]

    def run_decorator(self, callback):
        close_old_connections_and_discard(Mock(return_value={}), callback, Mock(), Mock(), Mock(), Mock(), BODY)

    def test_closes_connections(self):
        callback = Mock()

        self.run_decorator(callback)

        callback.assert_called_once()
        self.connection.close_if_unusable_or_obsolete.assert_called_once_with()
        self.nack.assert_not_called()

    def test_discards_message(self):
        def callback(*args):
            raise ValueError("anything")

        with self.assertLogs("yapw.decorators", level="ERROR"):
            self.run_decorator(callback)

        # `callback` isn't mocked.
        self.connection.close_if_unusable_or_obsolete.assert_called_once_with()
        self.assertEqual(self.nack.call_args.kwargs, {"requeue": False})
