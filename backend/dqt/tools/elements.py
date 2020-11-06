
from lxml import etree


# returns multiple elements
def multiple_line_elements(values):
    elements = []
    for value in values:
        element = etree.Element(
            '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p',
            attrib={'{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name': 'Standard'}
        )
        element.text = str(value)
        elements.append(element)

    return elements
