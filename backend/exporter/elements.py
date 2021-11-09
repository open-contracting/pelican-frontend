from lxml import etree


# returns one element
def image_element(image_file_path, aspect_ratio):
    image_element = etree.Element(
        "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}frame",
        attrib={
            # '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name': 'fr1',
            "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name": image_file_path,
            "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}anchor-type": "as-char",
            "{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width": "6.0cm",
            "{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height": "%fcm" % (6 * aspect_ratio),
            "{urn:oasis:names:tc:opendocument:xmlns:style:1.0}rel-width": "100%",
            "{urn:oasis:names:tc:opendocument:xmlns:style:1.0}rel-height": "scale",
            "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}z-index": "0",
        },
    )
    image_element.append(
        etree.Element(
            "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}image",
            attrib={
                "{http://www.w3.org/1999/xlink}href": image_file_path,
                "{http://www.w3.org/1999/xlink}type": "simple",
                "{http://www.w3.org/1999/xlink}show": "embed",
                "{http://www.w3.org/1999/xlink}actuate": "onLoad",
                "{urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0}mime-type": "image/png",
            },
        )
    )
    return image_element


# returns multiple elements
def multiple_line_elements(values):
    elements = []
    for value in values:
        element = etree.Element(
            "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p",
            attrib={"{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name": "Standard"},
        )
        element.text = str(value)
        elements.append(element)

    return elements
