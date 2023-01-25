from exporter.tag import LeafTag, TemplateTag
from exporter.util import quote_list


def template(_name, _default_template, _tags):
    """
    Build a :class:`~exporter.tag.TemplateTag` by decorating a
    :meth:`~exporter.tag.TemplateTag.get_context`` implementation.

    :param _name: the tag's name
    :param _default_template: the default value of the ``template`` argument
    :param _tags: the tag's sub-tags
    """

    def _template(function):
        class Tag(TemplateTag):
            name = _name
            argument_names = set()
            argument_required = set()
            argument_validators = {}
            argument_validation_messages = {}
            argument_converters = {}
            argument_defaults = {}

            default_template = _default_template
            tags = _tags

            def get_context(self):
                return function(self)

        return Tag

    return _template


def leaf(_name):
    """
    Build a :class:`~exporter.tag.LeafTag` by decorating a
    :meth:`~exporter.tag.LeafTag.render` implementation.

    :param _name: the tag's name
    """

    def _leaf(function):
        class Tag(LeafTag):
            name = _name
            argument_names = set()
            argument_required = set()
            argument_validators = {}
            argument_validation_messages = {}
            argument_converters = {}
            argument_defaults = {}

            def render(self, data):
                return function(self, data)

        return Tag

    return _leaf


def argument(name, default=None, required=False, choices=None, type=None, nonzero=False):
    """
    Add an argument to the tag.

    :param name: the argument's name
    :param default: the argument's default value
    :param required: whether the argument is required
    :param choices: the argument's allowed values
    :param type: the argument's allowed type
    :param nonzero: whether the argument can be 0 (if ``type=int``)
    """

    def _argument(cls):
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
