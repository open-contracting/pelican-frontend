
import re
import copy
import shortuuid

from lxml import etree
from dqt.tools.errors import TagError
from dqt.tools.misc import terms_enumeration


class LeafTag:
    def __init__(self, process_tag, value_type, gdocs, dataset_id):
        self.process_tag = process_tag
        if not (value_type == etree.Element or value_type == str):
            raise ValueError('Incorrect value type entered.')
        self.value_type = value_type
        self.gdocs = gdocs
        self.dataset_id = dataset_id

        self.param_validations_mapping = {}
        self.param_validations_description_mapping = {}
        self.params_mapping = {}
        self.required_params = set()

        self.required_data_fields = set()

    def set_param_validation(self, name, validation, description='The value must be in a valid format.', required=False):
        if name in self.param_validations_mapping:
            raise AttributeError('The parameter \'%s\' already exists.' % name)

        if required:
            self.required_params.add(name)

        self.param_validations_mapping[name] = validation
        self.param_validations_description_mapping[name] = description

    def set_required_data_field(self, name):
        if name in self.required_data_fields:
            raise AttributeError('%s data field already exists' % name)

        self.required_data_fields.add(name)

    def set_param(self, name, value):
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

    def get_param(self, name):
        if name in self.params_mapping:
            return self.params_mapping[name]
        else:
            return None

    def validate_and_process(self, data):
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

        return self.process_tag(data)


class TemplateTag:
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
        self.prepare_data = prepare_data
        self.base_template_id = base_template_id
        self.gdocs = gdocs
        self.dataset_id = dataset_id
        self.template = None
        self.param_validations_mapping = {}
        self.param_validations_description_mapping = {}
        self.params_mapping = {}
        self.required_params = set()
        self.sub_tags_mapping = {}

        self.set_param_validation(
            'template',
            lambda _: True,
            description='The value must be the id of the template file in Google Drive.',
        )

    def set_param_validation(self, name, validation, description='The value must be in a valid format.', required=False):
        if name in self.param_validations_mapping:
            raise AttributeError('The parameter \'%s\' already exists.' % name)

        if required:
            self.required_params.add(name)

        self.param_validations_mapping[name] = validation
        self.param_validations_description_mapping[name] = description

    def set_param(self, name, value):
        if name not in self.param_validations_mapping:
            if self.param_validations_mapping:
                suffix = 'Only the following parameters can be used for this tag: %s.' \
                    % terms_enumeration(self.param_validations_mapping)
            else:
                suffix = 'This tag does not use any parameters.'

            raise TagError(reason='The parameter \'%s\' is not supported. %s' % (name, suffix))

        if not self.param_validations_mapping[name](value):
            raise TagError(reason='The value \'%s\' for the parameter \'%s\' failed its validation. %s' % (
                value, name, self.param_validations_description_mapping[name]
            ))

        self.params_mapping[name] = value

    def get_param(self, name):
        if name in self.params_mapping:
            return self.params_mapping[name]
        else:
            return None

    def set_sub_tag(self, name, tag):
        if name in self.sub_tags_mapping:
            raise AttributeError('The sub-tag \'%s\'%s already exists' % name)

        self.sub_tags_mapping[name] = tag

    def get_sub_tag(self, name):
        if name in self.sub_tags_mapping:
            return self.sub_tags_mapping[name]
        else:
            return None

    def set_text(self, value, location):
        for node in self.template.xpath('.//*[contains(text(),"' + location + '")]'):
            if node.text and location in node.text:
                node.text = node.text.replace(location, str(value))
            else:
                for subnode in node:
                    if location in subnode.tail:
                        subnode.tail = subnode.tail.replace(location, str(value))

    def set_element(self, element, location):
        nodes = self.template.xpath('.//*[contains(text(),"' + location + '")]')
        while nodes:
            node = nodes[0]
            parent = node.getparent()

            if parent.tag == '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}text':
                wrapper_element = etree.Element(
                    '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p',
                    attrib={
                        '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name': 'Standard'
                    }
                )
                wrapper_element.append(element)
                node.addnext(copy.deepcopy(wrapper_element))
            else:
                node.addnext(copy.deepcopy(element))
            
            parent.remove(node)
            nodes = self.template.xpath('.//*[contains(text(),"' + location + '")]')

    def get_template_content(self, template):
        for node in template.xpath(
            '//office:text',
            namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
        ):
            return node

    def get_template_styles(self, template):
        for node in template.xpath(
            '//office:automatic-styles',
            namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
        ):
            return node

    def get_template_fonts(self, template):
        for node in template.xpath(
            '//office:font-face-decls',
            namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
        ):
            return node

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

    def merge_template(self, sub_template, location):
        prefix = shortuuid.uuid()
        sub_template_content = self.get_template_content(sub_template)
        for child in sub_template_content.iter():
            for attrib_name in child.attrib:
                if re.match(r'\{[^}]*\}style-name', attrib_name) and \
                        child.get(attrib_name) not in TemplateTag.DEFAULT_STYLES:
                    child.set(attrib_name, prefix + child.get(attrib_name))

        for location_node in self.template.xpath('.//*[contains(text(),"' + location + '")]'):
            parent = location_node.getparent()

            previous = location_node
            for child in sub_template_content:
                if "sequence-decls" in child.tag:
                    continue

                previous.addnext(child)
                previous = child

            # remove the template node
            parent.remove(location_node)

        self.merge_template_styles(sub_template, prefix)
        self.merge_template_fonts(sub_template)

    def get_tags_mapping(self):
        tags_mapping = {}

        xpath_term = './/*[namespace-uri()="urn:oasis:names:tc:opendocument:xmlns:text:1.0" and normalize-space(text())]/text()'
        for node in self.template.xpath(xpath_term):
            full_tags = re.findall(r'{%[^%}]+%}|{%[^%}]+$', node)

            for full_tag in full_tags:
                try:
                    tag_expression = TagExpression(full_tag)
                except TagError as er:
                    if not er.is_set():
                        er.set_full_tag(full_tag)
                        er.set_template_id(self.get_param('template'))
                    raise er

                tag_class = self.get_sub_tag(tag_expression.get_name())
                if tag_class is None:
                    raise TagError(
                        reason='The tag \'%s\' cannot be used in this context.' % tag_expression.get_name(),
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
                
                for param_name, param_value in tag_expression.get_params():
                    try:
                        tag.set_param(param_name, param_value)
                    except TagError as er:
                        if not er.is_set():
                            er.set_full_tag(full_tag)
                            er.set_template_id(self.get_param('template'))
                        raise er

                tags_mapping[full_tag] = tag

        return tags_mapping

    def validate_and_process(self):
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

        if self.get_param('template') is None:
            self.set_param('template', self.base_template_id)

        template_id = self.get_param('template')
        self.template = self.gdocs.get_template(template_id)
        data = self.prepare_data()

        tags_mapping = self.get_tags_mapping()
        for full_tag, tag in tags_mapping.items():
            if isinstance(tag, LeafTag):
                try:
                    result = tag.validate_and_process(data)
                except TagError as er:
                    if not er.is_set():
                        er.set_full_tag(full_tag)
                        er.set_template_id(self.get_param('template'))
                    raise er

                if tag.value_type == etree.Element:
                    self.set_element(result, full_tag)
                elif tag.value_type == str:
                    self.set_text(result, full_tag)
            elif isinstance(tag, TemplateTag):
                try:
                    result = tag.validate_and_process()
                except TagError as er:
                    if not er.is_set():
                        er.set_full_tag(full_tag)
                        er.set_template_id(self.get_param('template'))
                    raise er

                self.merge_template(result, full_tag)

        return self.template

class TagExpression:

    # full_tag must start with {%
    def __init__(self, full_tag):
        self.full_tag = full_tag
        self.name = None
        self.params_mapping = {}
        self.process()
        
    def process(self):
        if self.full_tag[-2:] != '%}':
            raise TagError(reason='The tag is incomplete. Please use the format for the tags: \
                {% <tag> <name>:|<value| <name>:|<value>| ... %}. \
                For a successful detection the whole tag must have the same formatting set. \
                Also, please check if the tag is spans one line only and each term is separated by one whitespace exactly.'
            )

        content = self.full_tag[2:-2].strip()
        terms = content.split()
        if not terms:
            raise TagError(reason='Tag with missing name.')

        self.name = terms[0]
        if not self.name.isalpha():
            raise TagError(reason='The tag name \'%s\' is incorrect. All characters must be alphabetic.' % self.name)
        
        param_expressions = terms[1:]
        for expr in param_expressions:
            result = re.search(r'^(\w+):\|([^|]+)\|$', expr)
            if not result:
                raise TagError(reason='The parameter expression \'%s\' is incorrect. Please use the following format: <name>:|<value>|.' % expr)
            
            param_name, param_value = result.groups()
            if not param_name.isalpha():
                raise TagError(reason='The parameter name \'%s\' is incorrect. All characters must be alphabetic.' % param_name)

            if param_name in self.params_mapping:
                raise TagError(reason='The parameter name \'%s\' is used multiple times.' % param_name)

            self.params_mapping[param_name] = param_value

    def get_name(self):
        return self.name

    def get_params(self):
        return list(self.params_mapping.items())
