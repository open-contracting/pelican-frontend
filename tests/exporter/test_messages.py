from unittest.mock import patch

from django.test import SimpleTestCase

from exporter.messages import MESSAGES, message, text


class TextTests(SimpleTestCase):
    def test_paragraphs(self):
        self.assertEqual(
            text("<p>One.</p><p>Two.</p>"),
            "One.\n\nTwo.",
        )

    def test_list(self):
        self.assertEqual(
            text("<p>One.</p><ul><li>First.</li><li>Second.</li></ul><p>Two.</p>"),
            "One.\n\n- First.\n- Second.\n\nTwo.",
        )

    def test_inline(self):
        self.assertEqual(
            text("The <code>tender.id</code> field <i>can</i> cost {'$'}1."),
            "The tender.id field can cost $1.",
        )


class MessageTests(SimpleTestCase):
    def test_message(self):
        self.assertEqual(
            message("en", "fieldDetail", "quality", "email", "name"),
            "Email address is valid",
        )

    def test_translated(self):
        self.assertEqual(
            message("es", "fieldDetail", "quality", "email", "name"),
            "La dirección de correo electrónico es válida",
        )

    @patch.dict(MESSAGES, {"es": {}})
    def test_untranslated(self):
        self.assertEqual(
            message("es", "fieldDetail", "quality", "email", "name"),
            "Email address is valid",
        )

    def test_unknown_language(self):
        self.assertEqual(
            message("fr", "fieldDetail", "quality", "email", "name"),
            "Email address is valid",
        )

    def test_unknown(self):
        self.assertEqual(
            message("en", "fieldDetail", "quality", "nonexistent", "name"),
            "fieldDetail.quality.nonexistent.name",
        )
