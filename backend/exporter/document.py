# All interactions with Open Document Format should be in this file.

import copy
import re
from dataclasses import dataclass

import shortuuid
from lxml import etree

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
    # "fr1",
)


def xpath(content: etree.Element, xpath: str) -> etree.Element:
    return content.xpath(xpath, namespaces={"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0"})


@dataclass
class Document:
    content: etree.Element

    def get_tags(self) -> etree.Element:
        return self.content.xpath('.//text()[contains(., "{%")]')

    # replaces all occurrences of full_tag with string value in the content
    def set_text(self, value: str, full_tag: str) -> None:
        nodes = self.content.xpath(FULL_TAG_LOCATION_XPATH.format(full_tag=full_tag))
        for node in nodes:
            if node.text:
                node.text = node.text.replace(full_tag, str(value))
            for child in node:
                if child.text:
                    child.text = child.text.replace(full_tag, str(value))  # probably unnecessary
                if child.tail:
                    child.tail = child.tail.replace(full_tag, str(value))

    # replaces all occurrences of full_tag with etree._Element value in the content
    # automatically wraps an element in <text:p>
    # if the node containing full_tag is not a <text:p> element the new element is added to the root of the document
    def set_element(self, element: etree.Element, full_tag: str) -> None:
        wrapper_element = etree.Element(
            "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p",
            attrib={"{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name": "Standard"},
        )
        wrapper_element.append(copy.deepcopy(element))

        nodes = self.content.xpath(FULL_TAG_LOCATION_XPATH.format(full_tag=full_tag))
        for node in nodes:
            if node.text:
                node.text = node.text.replace(full_tag, "")
            for child in node:
                if child.text:
                    child.text = child.text.replace(full_tag, "")  # probably unnecessary
                if child.tail:
                    child.tail = child.tail.replace(full_tag, "")

            if node.tag != "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p":
                parent = node.getparent()
                while parent.tag != "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}text":
                    node = parent
                    parent = node.getparent()

            node.addnext(copy.deepcopy(wrapper_element))

    # replaces all occurrences of full_tag with etree._Element values in the content
    # does not wrap each of the new elements in <text:p>
    # if the node containing full_tag is not a <text:p> element the new element is added to the root of the document
    def set_elements(self, elements: list[etree.Element], full_tag: str) -> None:
        nodes = self.content.xpath(FULL_TAG_LOCATION_XPATH.format(full_tag=full_tag))
        for node in nodes:
            if node.text:
                node.text = node.text.replace(full_tag, "")
            for child in node:
                if child.text:
                    child.text = child.text.replace(full_tag, "")  # probably unnecessary
                if child.tail:
                    child.tail = child.tail.replace(full_tag, "")

            if node.tag != "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p":
                parent = node.getparent()
                while parent.tag != "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}text":
                    node = parent
                    parent = node.getparent()

            current_node = node
            for element in elements:
                element_copy = copy.deepcopy(element)
                current_node.addnext(element_copy)
                current_node = element_copy

    def merge_styles(self, other: etree.Element, prefix: str) -> None:
        other_styles = xpath(other, "//office:automatic-styles")[0]

        for main_style_node in xpath(self.content, "//office:automatic-styles"):
            for sub_style in other_styles:
                # lets rename all paragraph styles to standard
                for attrib_name in list(sub_style.attrib.keys()):
                    if (
                        re.match(r"\{[^}]*\}(name|parent-style-name)", attrib_name)
                        and sub_style.get(attrib_name) not in DEFAULT_STYLES
                    ):
                        sub_style.set(attrib_name, prefix + sub_style.get(attrib_name))
                    elif re.match(r"\{[^}]*\}master-page-name", attrib_name):
                        sub_style.attrib.pop(attrib_name)

                main_style_node.append(sub_style)

    def merge_fonts(self, other: etree.Element) -> None:
        included_fonts = set()
        for child in xpath(self.content, "//office:font-face-decls")[0]:
            for attrib_name in child.attrib:
                if attrib_name.endswith("name"):
                    included_fonts.add(child.get(attrib_name))

        other_fonts = xpath(other, "//office:font-face-decls")[0]
        for main_font_node in xpath(self.content, "//office:font-face-decls"):
            for sub_font in other_fonts:
                for attrib_name in sub_font.attrib:
                    if re.match(r"\{[^}]*\}name", attrib_name) and sub_font.get(attrib_name) not in included_fonts:
                        main_font_node.append(sub_font)
                        break

    def merge(self, other: etree.Element, full_tag: str) -> None:
        prefix = shortuuid.uuid()
        other_content = xpath(other, "//office:text")[0]
        for child in other_content.iter():
            for attrib_name in child.attrib:
                if re.match(r"\{[^}]*\}style-name", attrib_name) and child.get(attrib_name) not in DEFAULT_STYLES:
                    child.set(attrib_name, prefix + child.get(attrib_name))

        nodes = self.content.xpath(FULL_TAG_LOCATION_XPATH.format(full_tag=full_tag))
        for node in nodes:
            if node.text:
                node.text = node.text.replace(full_tag, "")
            for child in node:
                if child.text:
                    child.text = child.text.replace(full_tag, "")  # probably unnecessary
                if child.tail:
                    child.tail = child.tail.replace(full_tag, "")

            parent = node.getparent()
            while parent.tag != "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}text":
                node = parent
                parent = node.getparent()

            previous = node
            for child in copy.deepcopy(other_content):
                if "sequence-decls" in child.tag:
                    continue

                previous.addnext(child)
                previous = child

        self.merge_styles(other, prefix)
        self.merge_fonts(other)
