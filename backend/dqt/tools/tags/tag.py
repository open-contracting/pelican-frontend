
import re
import copy
import shortuuid

from lxml import etree


class LeafTag:
    def __init__(self, process_tag, value_type, gdocs, dataset_id):
        self.process_tag = process_tag
        if not (value_type == etree.Element or value_type == str):
            raise ValueError('Incorrect value type entered')
        self.value_type = value_type
        self.gdocs = gdocs
        self.dataset_id = dataset_id

        self.param_validations_mapping = {}
        self.params_mapping = {}
        self.required_params = set()

    def set_param_validation(self, name, validation, required=False):
        if name in self.param_validations_mapping:
            raise AttributeError('%s param already exists' % name)

        if required:
            self.required_params.add(name)

        self.param_validations_mapping[name] = validation

    def set_param(self, name, value):
        if name not in self.param_validations_mapping:
            raise AttributeError('%s param is not supported' % name)

        if not self.param_validations_mapping[name](value):
            raise ValueError('The value %s for param %s failed its validation' % (value, name))

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
            raise AttributeError('Required params %s were not set' % list(missing_params))

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
        "fr1"
    )

    def __init__(self, prepare_data, base_template_id, gdocs, dataset_id):
        self.prepare_data = prepare_data
        self.base_template_id = base_template_id
        self.gdocs = gdocs
        self.dataset_id = dataset_id
        self.template = None
        self.param_validations_mapping = {}
        self.params_mapping = {}
        self.required_params = set()
        self.sub_tags_mapping = {}

        self.set_param_validation('template', lambda _: True)

    def set_param_validation(self, name, validation, required=False):
        if name in self.param_validations_mapping:
            raise AttributeError('%s param already exists' % name)

        if required:
            self.required_params.add(name)

        self.param_validations_mapping[name] = validation

    def set_param(self, name, value):
        if name not in self.param_validations_mapping:
            raise AttributeError('%s param is not supported' % name)

        if not self.param_validations_mapping[name](value):
            raise ValueError('The value %s for param %s failed its validation' % (value, name))

        self.params_mapping[name] = value

    def get_param(self, name):
        if name in self.params_mapping:
            return self.params_mapping[name]
        else:
            return None

    def set_sub_tag(self, name, tag):
        if name in self.sub_tags_mapping:
            raise AttributeError('%s sub tag already exists' % name)

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
            for index, child in enumerate(parent):
                if child == node:
                    parent.remove(child)
                    parent.insert(index, copy.deepcopy(element))
            
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

    def merge_template_styles(self, sub_template, prefix):
        sub_template_styles = self.get_template_styles(sub_template)

        for main_style_node in self.template.xpath(
            '//office:automatic-styles',
            namespaces={'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
        ):
            for sub_style in sub_template_styles:
                # lets rename all paragraph styles to standard
                for attrib in sub_style.attrib:
                    if attrib.endswith("name"):
                        sub_style.set(attrib, prefix + sub_style.get(attrib))

                main_style_node.append(sub_style)

    def merge_template(self, sub_template, location):
        prefix = shortuuid.uuid()
        sub_template_content = self.get_template_content(sub_template)
        for location_node in self.template.xpath('.//*[contains(text(),"' + location + '")]'):
            parent = location_node.getparent()

            previous = location_node
            for child in sub_template_content:
                if not "sequence-decls" in child.tag:
                    # lets rename all paragraph styles to standard
                    for attrib in child.attrib:
                        if "style-name" in attrib and child.get(attrib) == "P1":
                            child.set(attrib, "Standard")

                    for node in child:
                        for attrib in node.attrib:
                            if attrib.endswith("style-name"):
                                if node.get(attrib) not in TemplateTag.DEFAULT_STYLES:
                                    node.set(attrib, prefix + node.get(attrib))

                    previous.addnext(child)
                    previous = child

            # remove the template node
            parent.remove(location_node)

        self.merge_template_styles(sub_template, prefix)

    def get_tags_mapping(self):
        tags_mapping = {}

        for node in self.template.xpath('.//text()'):
            lines = re.findall("{%.*%}", node)

            for line in lines:
                tag_full = line
                line = line[2:-2]
                chunks = line.split()
                tag_name = chunks[0]

                tag_class = self.get_sub_tag(tag_name)
                if tag_class is None:
                    # TODO: better handling
                    continue

                tag = tag_class(self.gdocs, self.dataset_id)
                if len(chunks) > 1:
                    for chunk in chunks[1:]:
                        parts = chunk.split(':|')
                        param_name = parts[0]
                        if len(parts) > 1:
                            param_value = parts[1][:-1]
                        tag.set_param(param_name, param_value)

                tags_mapping[tag_full] = tag

        return tags_mapping

    def validate_and_process(self):
        missing_params = [
            name
            for name in self.required_params
            if name not in self.params_mapping
        ]
        if missing_params:
            raise AttributeError('Required params %s were not set' % list(missing_params))
        
        if self.get_param('template') is None:
            self.set_param('template', self.base_template_id)
        template_id = self.get_param('template')
        self.template = self.gdocs.get_template(template_id)
        tags_mapping = self.get_tags_mapping()
        data = self.prepare_data()

        for tag_full, tag in tags_mapping.items():
            if isinstance(tag, LeafTag):
                # TODO: catch errors
                result = tag.validate_and_process(data)
                if tag.value_type == etree.Element:
                    self.set_element(result, tag_full)
                elif tag.value_type == str:
                    self.set_text(result, tag_full)
            elif isinstance(tag, TemplateTag):
                # TODO: catch errors
                result = tag.validate_and_process()
                self.merge_template(result, tag_full)

        return self.template



