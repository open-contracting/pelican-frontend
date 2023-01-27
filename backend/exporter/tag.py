import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

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
from exporter.gdocs import Gdocs
from exporter.util import quote_list


class Tag:
    """
    A tag for inserting content into a template.

    :param gdocs: a Google API client
    :param dataset_id: the dataset's ID
    """

    #: The tag's name.
    name: Optional[str] = None
    #: The names of all arguments.
    argument_names: Set[str] = set()
    #: The names of required arguments.
    argument_required: Set[str] = set()
    #: A mapping of argument names to validation functions.
    argument_validators: Dict[str, Callable[[str], bool]] = {}
    #: A mapping of argument names to failure messages.
    argument_validation_messages: Dict[str, str] = {}
    #: A mapping of argument names to conversion functions.
    argument_converters: Dict[str, Callable[[str], Any]] = {}
    # . A mapping of argument names to default values.
    argument_defaults: Dict[str, Any] = {}

    def __init__(self, gdocs: Gdocs, dataset_id: int):
        self.gdocs = gdocs
        self.dataset_id = dataset_id
        self.arguments: Dict[str, Any] = {}

    # Do not call after `finalize_arguments`.
    def set_argument(self, name: str, value: Any) -> None:
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

    def finalize_arguments(self) -> None:
        """
        Set unused arguments to default values.

        :raises TagArgumentError: if a value is invalid
        """
        for name, default in self.argument_defaults.items():
            if name not in self.arguments:
                self.set_argument(name, default)

    # Do not call before `finalize_arguments`.
    def validate_and_render(self, data: Dict[str, Any]) -> Any:
        """
        Check for missing arguments, and call and return :meth:`~exporter.tag.Tag.render`.

        :raises MissingArgumentError: if arguments are missing
        """
        missing = [name for name in self.argument_required if name not in self.arguments]
        if missing:
            raise MissingArgumentError(f"Missing argument(s) for tag {self.name}: {quote_list(missing)}.")

        return self.render(data)

    def render(self, data: Dict[str, Any]) -> Any:
        """
        Render the tag.

        :param data: the data ("context") provided by another tag
        """
        raise NotImplementedError


# Keep this class, because render()'s signature differs between LeafTag and TemplateTag.
class LeafTag(Tag):
    """
    A leaf tag renders itself, using the data ("context") provided by a template tag.
    """

    def render(self, data: Dict[str, Any]) -> Union[str, etree.Element, List[etree.Element]]:
        """
        Render the tag.

        :param data: the data ("context") provided by a template tag
        """
        raise NotImplementedError


class TemplateTag(Tag):
    """
    A template tag renders a template, stored as a document in Google Docs. The template can contain sub-tags.

    :param gdocs: a Google API client
    :param dataset_id: the dataset's ID
    """

    #: The default value of the ``template`` argument.
    default_template: Optional[str] = None
    #: The sub-tags supported by the template tag.
    tags: Tuple[Type[Tag], ...] = ()

    def __init__(self, gdocs: Gdocs, dataset_id: int):
        super().__init__(gdocs, dataset_id)
        self.argument_names.add("template")
        self.argument_required.add("template")
        self.argument_defaults["template"] = self.default_template

    def get_context(self) -> Dict[str, Any]:
        """
        Return the data ("context") to be provided to sub-tags.
        """
        return {}

    def get_tags_mapping(self, texts: List[etree.Element]) -> Tuple[Dict[str, Tag], List[str]]:
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
                    f"The tag '{expression.name}' is not recognized. Please check the spelling and syntax.",
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

    def render(self, data: Dict[str, Any]) -> Tuple[etree.Element, List[str]]:
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
            if isinstance(tag, TemplateTag):
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
            else:
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

        return document.content, failed_tags


@dataclass
class TagExpression:
    """
    A representation of the tag as expressed in the template.

    :param name: The tag's name
    :param arguments: The tag's arguments
    """

    name: str
    arguments: Dict[str, str]

    @classmethod
    def parse(cls, string: str) -> "TagExpression":
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


def template(
    _name: str, _default_template: str, _tags: Tuple[Type[Tag], ...]
) -> Callable[[Callable[[TemplateTag], Dict[str, Any]]], Type[TemplateTag]]:
    """
    Build a :class:`~exporter.tag.TemplateTag` by decorating a
    :meth:`~exporter.tag.TemplateTag.get_context` implementation.

    :param _name: the tag's name
    :param _default_template: the default value of the ``template`` argument
    :param _tags: the tag's sub-tags
    """

    def _template(function: Callable[[TemplateTag], Dict[str, Any]]) -> Type[TemplateTag]:
        class _Tag(TemplateTag):
            name = _name
            argument_names = set()
            argument_required = set()
            argument_validators = {}
            argument_validation_messages = {}
            argument_converters = {}
            argument_defaults = {}

            default_template = _default_template
            tags = _tags

            def get_context(self) -> Dict[str, Any]:
                return function(self)

        return _Tag

    return _template


def leaf(
    _name: str,
) -> Callable[[Callable[[LeafTag, Dict[str, Any]], Union[str, etree.Element, List[etree.Element]]]], Type[LeafTag]]:
    """
    Build a :class:`~exporter.tag.LeafTag` by decorating a
    :meth:`~exporter.tag.LeafTag.render` implementation.

    :param _name: the tag's name
    """

    def _leaf(
        function: Callable[[LeafTag, Dict[str, Any]], Union[str, etree.Element, List[etree.Element]]]
    ) -> Type[LeafTag]:
        class _Tag(LeafTag):
            name = _name
            argument_names = set()
            argument_required = set()
            argument_validators = {}
            argument_validation_messages = {}
            argument_converters = {}
            argument_defaults = {}

            def render(self, data: Dict[str, Any]) -> Union[str, etree.Element, List[etree.Element]]:
                return function(self, data)

        return _Tag

    return _leaf


def argument(
    name: str,
    default: Optional[Any] = None,
    required: bool = False,
    choices: Optional[Union[Set[str], Dict[str, Any]]] = None,
    type: Optional[Type[int]] = None,
    nonzero: bool = False,
) -> Callable[[Type[Tag]], Type[Tag]]:
    """
    Add an argument to the tag.

    :param name: the argument's name
    :param default: the argument's default value
    :param required: whether the argument is required
    :param choices: the argument's allowed values
    :param type: the argument's allowed type
    :param nonzero: whether the argument can be 0 (if ``type=int``)
    """

    def _argument(cls: Type[Tag]) -> Type[Tag]:
        cls.argument_names.add(name)

        if default is not None:
            cls.argument_defaults[name] = default

        if required:
            cls.argument_required.add(name)

        if choices:
            cls.argument_validators[name] = lambda v: v in choices
            cls.argument_validation_messages[name] = "The value must be one of: %s." % quote_list(choices)

        if type is int:
            cls.argument_converters[name] = int
            if nonzero:
                cls.argument_validators[name] = lambda v: (isinstance(v, int) or v.isdigit()) and int(v) > 0
                cls.argument_validation_messages[name] = "The value must be a positive integer."
            else:
                cls.argument_validators[name] = lambda v: (isinstance(v, int) or v.isdigit()) and int(v) >= 0
                cls.argument_validation_messages[name] = "The value must be a non-negative integer."

        return cls

    return _argument


def generate_error_template_tag(message: str) -> Type[TemplateTag]:
    """
    Build a :class:`~exporter.tag.TemplateTag` for the error template and set the error ``message``.
    """

    @template("error", settings.GDOCS_TEMPLATES["DEFAULT_ERROR_TEMPLATE"], (value_tag,))
    def _tag(tag: TemplateTag) -> Dict[str, Any]:
        return {"value": message}

    return _tag


@leaf("value")
def value_tag(tag: LeafTag, data: Dict[str, Any]) -> str:
    return data["value"]
