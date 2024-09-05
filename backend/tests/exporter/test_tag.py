from django.test import SimpleTestCase
from exporter.exceptions import TagError
from exporter.tag import TagExpression


class TagExpressionTests(SimpleTestCase):
    def test_unclosed(self):
        with self.assertRaises(TagError) as cm:
            TagExpression.parse("{% name ")

        self.assertEqual(
            cm.exception.reason,
            "The tag is unclosed. Ensure the full tag is on one line, without style changes. Format: "
            "{% tag name1:|value1| name2:|value2| ... %}",
        )

    def test_empty(self):
        with self.assertRaises(TagError) as cm:
            TagExpression.parse("{% %}")

        self.assertEqual(cm.exception.reason, "The tag contains no tokens.")

    def test_malformed(self):
        with self.assertRaises(TagError) as cm:
            TagExpression.parse("{% name arg %}")

        self.assertEqual(cm.exception.reason, "The argument 'arg' is malformed. Format: name:|value|")

    def test_repeated(self):
        with self.assertRaises(TagError) as cm:
            TagExpression.parse("{% name arg:|val1| arg:|val2| %}")

        self.assertEqual(cm.exception.reason, "The argument 'arg' is repeated.")

    def test_sucess(self):
        raw_tag = TagExpression.parse("{% tagname arg1:|val1| arg2:|val2| %}")

        self.assertEqual(raw_tag.name, "tagname")
        self.assertEqual(raw_tag.arguments, {"arg1": "val1", "arg2": "val2"})
