import re

from django.test import SimpleTestCase

from exporter.messages import DEFAULT_LANGUAGE, DISCARDED_TAGS, MESSAGES, SUBSTITUTIONS

ELEMENT = re.compile(r"</?\w+>")
PLACEHOLDER = re.compile(r"\{'\$'\}|\{\w+\}")
CODE = re.compile(r"<code>.*?</code>")
# The exporter reads a check's name and description, and no other message.
EXPORTED = re.compile(r"^(?:datasetLevel|resourceLevel|fieldDetail)\.\w+\.\w+\.(?:name|description)$")


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

    def test_exported_markup(self):
        """A message the exporter reads uses only the markup its plain text conversion covers."""
        for language, catalog in ({DEFAULT_LANGUAGE: english} | translations).items():
            for key, message in catalog.items():
                if not EXPORTED.match(key):
                    continue
                for element in ELEMENT.findall(message):
                    with self.subTest(language=language, key=key, element=element):
                        self.assertTrue(DISCARDED_TAGS.fullmatch(element) or element in SUBSTITUTIONS)
