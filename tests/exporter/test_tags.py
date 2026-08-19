from django.test import SimpleTestCase

from exporter.exceptions import TagError
from exporter.leaf_tags.field import name

data = {"path": "ocid", "qualityCheck": "ocid_prefix_check"}


def get_tag(arguments, language="en"):
    tag = name("Gdocs", 1, language)
    for key, value in arguments.items():
        tag.set_argument(key, value)
    tag.finalize_arguments()
    return tag


class Tests(SimpleTestCase):
    def test_required(self):
        with self.assertRaises(TagError) as cm:
            get_tag({}).validate_and_render(data)

        self.assertEqual(cm.exception.reason, "Missing argument(s) for tag name: 'level'.")

    def test_invalid(self):
        with self.assertRaises(TagError) as cm:
            get_tag({"invalid": ""}).validate_and_render(data)

        self.assertEqual(
            cm.exception.reason,
            "The argument 'invalid' is not valid. The argument must be one of: 'level'.",
        )

    def test_choices(self):
        with self.assertRaises(TagError) as cm:
            get_tag({"level": "invalid"}).validate_and_render(data)

        self.assertEqual(
            cm.exception.reason,
            "The value 'invalid' for argument 'level' is not valid. The value must be one of: "
            "'coverageEmpty', 'coverageSet', 'quality'.",
        )

    def test_success(self):
        for level, expected in (
            ("coverageEmpty", "Field isn't null or empty"),
            ("coverageSet", "Field is set"),
            ("quality", "OCID prefix is registered"),
        ):
            with self.subTest(level=level):
                self.assertEqual(get_tag({"level": level}).validate_and_render(data), expected)

    def test_success_translated(self):
        tag = get_tag({"level": "coverageSet"}, language="es")
        self.assertEqual(tag.validate_and_render(data), "El campo está establecido")
