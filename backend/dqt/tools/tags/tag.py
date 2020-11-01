
import re
import copy
import shortuuid

from lxml import etree
from dqt.tools.errors import TagError
from dqt.tools.misc import terms_enumeration

# General tag class representing all kinds of tags, that can occur (TemplateTag, LeafTag, ...)
class Tag:
    def __init__(self, gdocs, dataset_id):
        self.gdocs = gdocs
        self.dataset_id = dataset_id

        self.params_finalized = False
        self.param_validations_mapping = {}
        self.param_validations_description_mapping = {}
        self.params_mapping = {}
        self.required_params = set()

        self.required_data_fields = set()

    # adds new param with its validation function
    def set_param_validation(self, name, validation, description='The value must be in a valid format.', required=False):
        if self.params_finalized:
            raise ValueError('The parameters for this tag have been already finalized. New parameter validations cannot be set.')

        if name in self.param_validations_mapping:
            raise AttributeError('The parameter \'%s\' already exists.' % name)

        if required:
            self.required_params.add(name)

        self.param_validations_mapping[name] = validation
        self.param_validations_description_mapping[name] = description

    # adds new field requirement that is must be passed to the tag for its correct function
    def set_required_data_field(self, name):
        if name in self.required_data_fields:
            raise AttributeError('%s data field already exists' % name)

        self.required_data_fields.add(name)

    # sets parameter value; raises an exception when the params have already been finalized
    def set_param(self, name, value):
        if self.params_finalized:
            raise ValueError('The parameters for this tag have been already finalized. New parameter values cannot be set.')

        if name not in self.param_validations_mapping:
            if self.param_validations_mapping:
                suffix = 'Only the following parameters can be used for this tag: %s.' \
                    % terms_enumeration(self.param_validations_mapping)
            else:
                suffix = 'This tag does not use any parameters.'

            raise TagError(reason='The parameter \'%s\' is not supported. %s' % (name, suffix))

        if not self.param_validations_mapping[name](value):
            raise TagError(reason='The value \'%s\' for parameter \'%s\' failed validation. %s' % (
                value, name, self.param_validations_description_mapping[name]
            ))

        self.params_mapping[name] = value

    # retrieves respective parameter if set, otherwise None
    def get_param(self, name):
        if name in self.params_mapping:
            return self.params_mapping[name]
        else:
            return None

    # after param finalization new params cannot added nor set
    def finalize_params(self):
        self.params_finalized = True

    # validates tag params, its values; can be performed only when params have been finalized
    def validate(self, data):
        if not self.params_finalized:
            raise ValueError('The parameters for this tag have not been finalized yet. Validation cannot be executed.')

        missing_params = [
            name
            for name in self.required_params
            if name not in self.params_mapping
        ]
        if missing_params:
            if len(missing_params) == 1:
                raise TagError(reason='The required parameter \'%s\' was not set.' % missing_params[0])
            else:
                missing_params_str = ', '.join('\'%s\'' % param for param in missing_params)
                raise TagError(reason='The required parameters %s were not set.' % missing_params_str)

        missing_data_fields = [
            name
            for name in self.required_data_fields
            if name not in data
        ]
        if missing_data_fields:
            raise AttributeError('The required data fields %s were not set' % list(missing_data_fields))

# LeafTag can only be at the end of the whole tree of tags
# LeafTag accepts data from its parent tag and returns either a string value or an etree._Element
class LeafTag(Tag):
    def __init__(self, process_tag, gdocs, dataset_id):
        super().__init__(gdocs, dataset_id)
        self.process_tag = process_tag

    def validate_and_process(self, data):
        self.validate(data)
        return self.process_tag(data)

# TemplateTag signifies a context in which other tags can occur
# It seeks its child tags in a google doc file that is retrieved using the template id
class TemplateTag(Tag):
    TAG_EXPRESSION_XPATH = './/text()[contains(., "{%")]'
    FULL_TAG_LOCATION_XPATH = './/*[.//text()[contains(., "{full_tag}")] and not(./*//text()[contains(., "{full_tag}")])]'
    DEFAULT_STYLES = (
        "Standard",
        "Heading",
        "Text_20_body",
        "List",
        "Caption",
        "Index",
        "normal",
        "Heading_20_1",
        "Heading_20_2",
        "Heading_20_3",
        "Heading_20_4",
        "Heading_20_5",
        "Heading_20_6",
        "Title",
        "Subtitle",
        "Header",
        "Graphics",
        # "fr1"
    )

    def __init__(self, prepare_data, base_template_id, gdocs, dataset_id):
        super().__init__(gdocs, dataset_id)
        self.prepare_data = prepare_data # the main method that is called in validate_and_process
        self.base_template_id = base_template_id # in case no template id is specified explicitly
        self.template = None
        self.sub_tags_mapping = {}

        self.set_param_validation(
            'template',
            lambda _: True,
            description='The value must be the id of the template file in Google Drive.',
            required=True
        )

    # overrides original finalize_params method
    def finalize_params(self):
        if self.get_param('template') is None:
            self.set_param('template', self.base_template_id)

        super().finalize_params()

    # adds new sub tag
    def set_sub_tag(self, name, tag):
        if name in self.sub_tags_mapping:
            raise AttributeError('The sub-tag \'%s\'%s already exists' % name)

        self.sub_tags_mapping[name] = tag

    # retrieves respective tag if set, otherwise None
    def get_sub_tag(self, name):
        if name in self.sub_tags_mapping:
            return self.sub_tags_mapping[name]
        else:
            return None

    # replaces all occurrences of full_tag with string value in the template
    def set_text(self, value, full_tag):
        nodes = self.template.xpath(TemplateTag.FULL_TAG_LOCATION_XPATH.format(full_tag=full_tag))
        for node in nodes:
            if node.text:
                node.text = node.text.replace(full_tag, str(value))
            for child in node:
                if child.text:
                    child.text = child.text.replace(full_tag, str(value)) # probably unnecessary
                if child.tail:
                    child.tail = child.tail.replace(full_tag, str(value))

    # replaces all occurrences of full_tag with etree._Element value in the template
    # some elements need a specific wrapper to be displayed correctly
    def set_element(self, element, full_tag, wrap=True):
        if wrap:
            wrapper_element = etree.Element(
                '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p',
                attrib={
                    '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name': 'Standard'
                }
            )
            wrapper_element.append(copy.deepcopy(element))
        else:
            wrapper_element = copy.deepcopy(element)

        nodes = self.template.xpath(TemplateTag.FULL_TAG_LOCATION_XPATH.format(full_tag=full_tag))
        for node in nodes: 
            if node.text:
                node.text = node.text.replace(full_tag, '')
            for child in node:
                if child.text:
                    child.text = child.text.replace(full_tag, '') # probably unnecessary
                if child.tail:
                    child.tail = child.tail.replace(full_tag, '')

            if node.tag != '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p':
                parent = node.getparent()
                while parent.tag != '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}text':
                    node = parent
                    parent = node.getparent()
            
            node.addnext(copy.deepcopy(wrapper_element))

    def get_template_content(self, template):
        return template.xpath(
            '//office:text',
            namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
        )[0]

    def get_template_styles(self, template):
        return template.xpath(
            '//office:automatic-styles',
            namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
        )[0]

    def get_template_fonts(self, template):
        return template.xpath(
            '//office:font-face-decls',
            namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
        )[0]

    def merge_template_styles(self, sub_template, prefix):
        sub_template_styles = self.get_template_styles(sub_template)

        for main_style_node in self.template.xpath(
            '//office:automatic-styles',
            namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
        ):
            for sub_style in sub_template_styles:
                # lets rename all paragraph styles to standard
                for attrib_name in list(sub_style.attrib.keys()):
                    if re.match(r'\{[^}]*\}(name|parent-style-name)', attrib_name) and \
                            sub_style.get(attrib_name) not in TemplateTag.DEFAULT_STYLES:
                        sub_style.set(attrib_name, prefix + sub_style.get(attrib_name))
                    elif re.match(r'\{[^}]*\}master-page-name', attrib_name):
                        sub_style.attrib.pop(attrib_name)

                main_style_node.append(sub_style)

    def merge_template_fonts(self, sub_tempalte):
        included_fonts = set()
        for child in self.get_template_fonts(self.template):
            for attrib_name in child.attrib:
                if attrib_name.endswith('name'):
                    included_fonts.add(child.get(attrib_name))

        sub_template_fonts = self.get_template_fonts(sub_tempalte)
        for main_font_node in self.template.xpath(
            '//office:font-face-decls',
            namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
        ):
            for sub_font in sub_template_fonts:
                for attrib_name in sub_font.attrib:
                    if re.match(r'\{[^}]*\}name', attrib_name) and \
                            sub_font.get(attrib_name) not in included_fonts:
                        main_font_node.append(sub_font)
                        break

    def merge_template(self, sub_template, full_tag):
        prefix = shortuuid.uuid()
        sub_template_content = self.get_template_content(sub_template)
        for child in sub_template_content.iter():
            for attrib_name in child.attrib:
                if re.match(r'\{[^}]*\}style-name', attrib_name) and \
                        child.get(attrib_name) not in TemplateTag.DEFAULT_STYLES:
                    child.set(attrib_name, prefix + child.get(attrib_name))

        nodes = self.template.xpath(TemplateTag.FULL_TAG_LOCATION_XPATH.format(full_tag=full_tag))
        for node in nodes:
            if node.text:
                node.text = node.text.replace(full_tag, '')
            for child in node:
                if child.text:
                    child.text = child.text.replace(full_tag, '') # probably unnecessary
                if child.tail:
                    child.tail = child.tail.replace(full_tag, '')

            parent = node.getparent()
            while parent.tag != '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}text':
                node = parent
                parent = node.getparent()

            previous = node
            for child in copy.deepcopy(sub_template_content):
                if "sequence-decls" in child.tag:
                    continue

                previous.addnext(child)
                previous = child

        self.merge_template_styles(sub_template, prefix)
        self.merge_template_fonts(sub_template)

    # searches for tags in the template and sets their params
    def get_tags_mapping(self):
        tags_mapping = {}

        full_tags = set()
        texts = self.template.xpath(TemplateTag.TAG_EXPRESSION_XPATH)
        for text in texts:
            full_tags.update(re.findall(r'{%[^%}]+%}|{%[^%}]+$', text))

        for full_tag in full_tags:
            try:
                tag_expression = TagExpression(full_tag)
            except TagError as er:
                if not er.is_set():
                    er.set_full_tag(full_tag)
                    er.set_template_id(self.get_param('template'))
                raise er

            if not tag_expression.has_tag_chaining():
                tag_class = self.get_sub_tag(tag_expression.get_tag_name(0))
                if tag_class is None:
                    raise TagError(
                        reason='The tag \'%s\' cannot be used in this context. Also, please make sure the check was computed.' % tag_expression.get_tag_name(0),
                        full_tag=full_tag,
                        template_id=self.get_param('template')
                    )

                try:
                    tag = tag_class(self.gdocs, self.dataset_id)
                except TagError as er:
                    if not er.is_set():
                        er.set_full_tag(full_tag)
                        er.set_template_id(self.get_param('template'))
                    raise er

                for param_name, param_value in tag_expression.get_tag_params(0):
                    try:
                        tag.set_param(param_name, param_value)
                    except TagError as er:
                        if not er.is_set():
                            er.set_full_tag(full_tag)
                            er.set_template_id(self.get_param('template'))
                        raise er
                tag.finalize_params()
            else:
                try:
                    tag_chaining = TagChaining(self, tag_expression)
                    tag = tag_chaining.generate_tag_class()(self.gdocs, self.dataset_id)
                except TagError as er:
                    if not er.is_set():
                        er.set_full_tag(full_tag)
                        er.set_template_id(self.get_param('template'))
                    raise er

            tags_mapping[full_tag] = tag

        return tags_mapping

    # recursive method that calls sub tags' validate_and_process methods and incorporates the result in the template
    def validate_and_process(self, data):
        self.validate(data)

        self.template = self.gdocs.get_template(self.get_param('template'))
        new_data = self.prepare_data(data)

        tags_mapping = self.get_tags_mapping()
        for full_tag, tag in tags_mapping.items():
            if isinstance(tag, LeafTag):
                try:
                    result = tag.validate_and_process(new_data)
                except TagError as er:
                    if not er.is_set():
                        er.set_full_tag(full_tag)
                        er.set_template_id(self.get_param('template'))
                    raise er
                
                if isinstance(result, etree._Element):
                    self.set_element(result, full_tag)
                elif isinstance(result, str):
                    self.set_text(result, full_tag)
                else:
                    raise ValueError('LeafTag\'s process_tag method must return of the following types: \'etree.Element\', \'str\'.')

            elif isinstance(tag, TemplateTag):
                try:
                    result = tag.validate_and_process(new_data)
                except TagError as er:
                    if not er.is_set():
                        er.set_full_tag(full_tag)
                        er.set_template_id(self.get_param('template'))
                    raise er

                self.merge_template(result, full_tag)

        return self.template

# TagExpression represents the literal tag as it occurs in the template
class TagExpression:
    # full_tag must start with {%
    def __init__(self, full_tag):
        self.full_tag = full_tag
        self.tag_names = []
        self.tag_param_mappings = []
        self.process()

    # processes the tag
    # in the case of incompletness or incorrect composition TagError is raised
    def process(self):
        if self.full_tag[-2:] != '%}':
            raise TagError(reason='The tag is incomplete. Please use the format for the tags: \
                {% <tag> <name>:|<value| <name>:|<value>| ... %}. \
                For a successful detection the whole tag must have the same formatting set. \
                Also, please check if the tag is spans one line only and each term is separated by one whitespace exactly.'
            )

        content = self.full_tag[2:-2].strip()
        for tag in content.split('->'):
            terms = [term.strip() for term in tag.split()]
            if not terms:
                raise TagError(reason='Tag with missing name.')

            tag_name = terms[0]
            if not tag_name:
                raise TagError(reason='The tag name \'%s\' is incorrect. All characters must be alphabetic.' % tag_name)

            tag_param_mapping = {}
            param_expressions = terms[1:]
            for expr in param_expressions:
                result = re.search(r'^(\w+):\|([^|]+)\|$', expr)
                if not result:
                    raise TagError(reason='The parameter expression \'%s\' is incorrect. Please use the following format: <name>:|<value>|.' % expr)

                param_name, param_value = result.groups()
                if not param_name.isalpha():
                    raise TagError(reason='The parameter name \'%s\' is incorrect. All characters must be alphabetic.' % param_name)

                if param_name in tag_param_mapping:
                    raise TagError(reason='The parameter name \'%s\' is used multiple times.' % param_name)

                tag_param_mapping[param_name] = param_value

            self.tag_names.append(tag_name)
            self.tag_param_mappings.append(tag_param_mapping)

    def get_tag_name(self, index):
        return self.tag_names[index]

    def get_tag_params(self, index):
        return list(self.tag_param_mappings[index].items())

    def get_tag_count(self):
        return len(self.tag_names)

    def has_tag_chaining(self):
        return len(self.tag_names) > 1

# processes tag expression with tag chaining, i.e. {% <tag> -> <sub tag> %}
class TagChaining:
    def __init__(self, source_tag, tag_expression):
        self.source_tag = source_tag
        self.tag_expression = tag_expression
        self.chained_tags = []

        self.create_chained_tags()

    def create_chained_tags(self):
        tag_count = self.tag_expression.get_tag_count()
        previous_tag = self.source_tag
        for current_tag_index in range(tag_count):
            current_tag_name = self.tag_expression.get_tag_name(current_tag_index)
            current_tag_params = self.tag_expression.get_tag_params(current_tag_index)

            current_tag_class = previous_tag.get_sub_tag(current_tag_name)
            if current_tag_class is None:
                raise TagError(
                    reason='Wrong tag chaining. The tag \'%s\' cannot be used in this context. Also, please make sure the check was computed.' % current_tag_name,
                )

            if current_tag_index < (tag_count - 1) and not issubclass(current_tag_class, TemplateTag):
                raise TagError(
                    reason='Wrong tag chaining. The tag \'%s\' is not a template tag and thus cannot be followed by another tag.' % current_tag_name
                )

            current_tag = current_tag_class(self.source_tag.gdocs, self.source_tag.dataset_id)
            for param_name, param_value in current_tag_params:
                current_tag.set_param(param_name, param_value)
            current_tag.finalize_params()

            self.chained_tags.append(current_tag)
            previous_tag = current_tag

    def generate_tag_class(self):
        chained_tags = self.chained_tags
        last_tag = self.chained_tags[-1]
        if isinstance(last_tag, LeafTag):
            class GeneratedTag(LeafTag):
                def __init__(self, gdocs, dataset_id):
                    pass

                def validate_and_process(self, data):
                    for tag in chained_tags[:-1]:
                        tag.validate(data)
                        data = tag.prepare_data(data)

                    return last_tag.validate_and_process(data)

        elif isinstance(last_tag, TemplateTag):
            class GeneratedTag(TemplateTag):
                def __init__(self, gdocs, dataset_id):
                    pass

                def validate_and_process(self, data):
                    for tag in chained_tags[:-1]:
                        tag.validate(data)
                        data = tag.prepare_data(data)

                    return last_tag.validate_and_process(data)

        else:
            raise NotImplemented('Tag generation for instance of \'%s\' is not supported.' % type(last_tag).__name__)

        return GeneratedTag
