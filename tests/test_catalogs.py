import re

from django.test import SimpleTestCase

from exporter.messages import DEFAULT_LANGUAGE, MESSAGES

ELEMENT = re.compile(r"</?\w+>")
PLACEHOLDER = re.compile(r"\{'\$'\}|\{\w+\}")
CODE = re.compile(r"<code>.*?</code>")


def flatten(node, prefix=""):
    """Return a catalog as a mapping of dotted key to message, in the order the file declares them."""
    messages = {}
    for key, value in node.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            messages.update(flatten(value, path))
        else:
            messages[path] = value
    return messages


english = flatten(MESSAGES[DEFAULT_LANGUAGE])
translations = {language: flatten(catalog) for language, catalog in MESSAGES.items() if language != DEFAULT_LANGUAGE}


class CatalogTests(SimpleTestCase):
    def test_complete(self):
        for language, catalog in translations.items():
            with self.subTest(language=language):
                self.assertEqual(set(catalog), set(english))

    def test_ordered(self):
        for language, catalog in translations.items():
            with self.subTest(language=language):
                self.assertEqual(list(catalog), list(english))

    def test_elements(self):
        for language, catalog in translations.items():
            for key, message in catalog.items():
                with self.subTest(language=language, key=key):
                    self.assertCountEqual(ELEMENT.findall(message), ELEMENT.findall(english[key]))

    def test_placeholders(self):
        for language, catalog in translations.items():
            for key, message in catalog.items():
                with self.subTest(language=language, key=key):
                    self.assertCountEqual(PLACEHOLDER.findall(message), PLACEHOLDER.findall(english[key]))

    def test_code(self):
        for language, catalog in translations.items():
            for key, message in catalog.items():
                with self.subTest(language=language, key=key):
                    self.assertCountEqual(CODE.findall(message), CODE.findall(english[key]))
