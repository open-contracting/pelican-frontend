import re
from dataclasses import dataclass

from django.conf import settings
from lxml import etree

from exporter.document import Document
from exporter.exceptions import (
    CheckNotComputedError,
    MissingArgumentError,
    TagArgumentError,
    TagError,
    TagSyntaxError,
    UnknownTagError,
)
from exporter.util import quote_list


class Tag:
    """
    A tag for inserting content into a template.
    """

    #: The tag's name.
    name = None
    #: The names of all arguments.
    argument_names = set()
    #: The names of required arguments.
    argument_required = set()
    #: A mapping of argument names to validation functions.
    argument_validators = {}
    #: A mapping of argument names to failure messages.
    argument_validation_messages = {}
    #: A mapping of argument names to conversion functions.
    argument_converters = {}
    # . A mapping of argument names to default values.
    argument_defaults = {}

    def __init__(self, gdocs, dataset_id):
        self.gdocs = gdocs
        self.dataset_id = dataset_id
        self.arguments = {}

    # Do not call after `finalize_arguments`.
    def set_argument(self, name, value):
        """
        Set an argument.

        The argument's name is checked against declared arguments, and its value is checked with the declared
        validator, if any. Its value is converted with the declared converter, if any.

        :param name: the argument's name
        :param value: the argument's value
        :raises TagArgumentError: if the name is unrecognized or the value is invalid
        """
        if name not in self.argument_names:
            if self.argument_names:
                suffix = f"The argument must be one of: {quote_list(self.argument_names)}."
            else:
                suffix = "This tag does not accept any arguments."

            raise TagArgumentError(f"The argument '{name}' is not valid. {suffix}")

        if name in self.argument_validators and not self.argument_validators[name](value):
            raise TagArgumentError(
                f"The value '{value}' for argument '{name}' is not valid. {self.argument_validation_messages[name]}"
            )

        if name in self.argument_converters:
            value = self.argument_converters[name](value)

        self.arguments[name] = value

    def finalize_arguments(self):
        """
        Set unused arguments to default values.

        :raises TagArgumentError: if a value is invalid
        """
        for name, default in self.argument_defaults.items():
            if name not in self.arguments:
                self.set_argument(name, default)

    # Do not call before `finalize_arguments`.
    def validate_and_render(self, data):
        """
        Check for missing arguments, and call and return :meth:`~exporter.tag.Tag.render`.

        :raises MissingArgumentError: if arguments are missing
        """
        missing = [name for name in self.argument_required if name not in self.arguments]
        if missing:
            raise MissingArgumentError(f"Missing argument(s) for tag {self.name}: {quote_list(missing)}.")

        return self.render(data)


class LeafTag(Tag):
    """
    A leaf tag renders itself, using the data ("context") provided by a template tag.
    """

    def render(self, data):
        """
        Render the tag, as a string, ``etree._Element`` or list of ``etree._Element``.

        :param data: the data ("context") provided by a template tag
        """
        raise NotImplementedError


class TemplateTag(Tag):
    """
    A template tag renders a template, stored as a document in Google Docs. The template can contain sub-tags.
    """

    #: The default value of the ``template`` argument.
    default_template = None
    #: The sub-tags supported by the template tag.
    tags = ()

    def __init__(self, gdocs, dataset_id):
        super().__init__(gdocs, dataset_id)
        self.argument_names.add("template")
        self.argument_required.add("template")
        self.argument_defaults["template"] = self.default_template

    def get_context(self):
        """
        Return the data ("context") to be provided to sub-tags.
        """
        return {}

    def get_tags_mapping(self, texts):
        """
        Extract and instantiate the tags in the template.

        Also return the names of any checks that cannot be computed. The corresponding tags are replaced with
        :func:`error template tags<exporter.tag.generate_error_template_tag>`.

        :param texts: the text nodes from the template that contain tags
        :raises TagSyntaxError: if a sub-tag is malformed
        :raises UnknownTagError: if a sub-tag's name is unrecognized
        :raises TagArgumentError: if a sub-tag's argument is invalid
        """
        tags_lookup = {tag.name: tag for tag in self.tags}

        tags_mapping = {}
        failed_tags = []

        full_tags = set()
        for text in texts:
            full_tags.update(re.findall(r"{%[^%}]+%}|{%[^%}]+$", text))

        for full_tag in full_tags:
            try:
                expression = TagExpression.parse(full_tag)
            except TagSyntaxError as er:
                raise er.fill(full_tag, self.arguments["template"])

            tag_class = tags_lookup.get(expression.name)
            if tag_class is None:
                raise UnknownTagError(
                    f"The tag '{expression.name}' cannot be used in this context. "
                    "Also, please make sure the check was computed.",
                    full_tag,
                    self.arguments["template"],
                )

            tag = tag_class(self.gdocs, self.dataset_id)

            for name, value in expression.arguments.items():
                try:
                    tag.set_argument(name, value)
                except TagArgumentError as er:
                    raise er.fill(full_tag, self.arguments["template"])

            try:
                tag.finalize_arguments()
            except CheckNotComputedError as er:
                tag = generate_error_template_tag(
                    f"WARNING: Check {str(er)} was not computed. Please check your dataset.",
                )(self.gdocs, self.dataset_id)
                tag.finalize_arguments()
                failed_tags.append(str(er))

            tags_mapping[full_tag] = tag

        return tags_mapping, failed_tags

    def render(self, data):
        """
        Read the template's content, extract its sub-tags, recursively call the sub-tags'
        :meth:`~exporter.tag.Tag.validate_and_render` method, and merge the results into the content.

        :param data: the data ("context") provided by another template tag
        :raises MissingArgumentError: if a leaf tag's argument is missing
        :raises ValueError: if a leaf tag's :meth:`~exporter.tag.LeafTag.render` method has an invalid return value
        :raises TagError: if a template tag or its sub-tags caused an error
        """
        document = Document(self.gdocs.get_content(self.arguments["template"]))
        new_data = self.get_context()

        tags_mapping, failed_tags = self.get_tags_mapping(document.get_tags())

        for full_tag, tag in tags_mapping.items():
            if isinstance(tag, LeafTag):
                try:
                    result = tag.validate_and_render(new_data)
                except MissingArgumentError as er:
                    raise er.fill(full_tag, self.arguments["template"])

                if isinstance(result, list) and all(isinstance(el, etree._Element) for el in result):
                    document.set_elements(result, full_tag)
                elif isinstance(result, etree._Element):
                    document.set_element(result, full_tag)
                elif isinstance(result, str):
                    document.set_text(result, full_tag)
                else:
                    raise ValueError(
                        "LeafTag's render method must return of the following types: "
                        "list of 'etree.Element', 'etree.Element', 'str'."
                    )
            elif isinstance(tag, TemplateTag):
                try:
                    result, sub_failed_tags = tag.validate_and_render(new_data)
                    failed_tags += sub_failed_tags
                except TagError as er:
                    raise er.fill(full_tag, self.arguments["template"])
                except CheckNotComputedError as er:
                    document.set_text("Element could not be computed", full_tag)
                    failed_tags.append(str(er))
                    continue
                document.merge(result, full_tag)

        return document.content, failed_tags


@dataclass
class TagExpression:
    """
    A representation of the tag as expressed in the template.
    """

    #: The tag's name
    name: str
    #: The tag's arguments
    arguments: dict

    @classmethod
    def parse(cls, string):
        """
        Parse the string as a tag.

        :param string: the full tag, starting with ``{%``
        :raises TagSyntaxError: if the tag is malformed
        """
        if string[-2:] != "%}":
            raise TagSyntaxError(
                "The tag is unclosed. Ensure the full tag is on one line, without style changes. Format: "
                "{% tag name1:|value1| name2:|value2| ... %}"
            )

        tokens = string[2:-2].split()
        if not tokens:
            raise TagSyntaxError("The tag contains no tokens.")

        arguments = {}
        for token in tokens[1:]:
            match = re.search(r"^(\w+):\|([^|]+)\|$", token)
            if not match:
                raise TagSyntaxError(f"The argument '{token}' is malformed. Format: name:|value|")

            name, value = match.groups()
            if name in arguments:
                raise TagSyntaxError(f"The argument '{name}' is repeated.")

            arguments[name] = value

        return cls(tokens[0], arguments)


def generate_error_template_tag(message):
    """
    Build a :class:`~exporter.tag.TemplateTag` for the error template and set the error message.

    :param message: the error message to store in the tag's context
    """

    class Tag(TemplateTag):
        name = "error"

        default_template = settings.GDOCS_TEMPLATES["DEFAULT_ERROR_TEMPLATE"]
        tags = (ValueTag,)

        def get_context(self):
            return {"value": message}

    return Tag


class ValueTag(LeafTag):
    """
    A tag that returns the "value" key from the context.
    """

    name = "value"

    def render(self, data):
        return data["value"]
