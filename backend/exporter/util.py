import random

from lxml import etree

LEVELS = {"coverage", "coverageSet", "coverageEmpty", "quality"}
MODES = {"oneLine", "multipleLines"}


def quote_list(it):
    return ", ".join(f"'{el}'" for el in sorted(it))


def sample_and_format(population, arguments):
    length = len(population)
    examples = random.sample(population, k=min(length, arguments.get("max", length)))

    if arguments["mode"] == "oneLine":
        return ", ".join(examples)
    return multiple_line_elements(examples)


def box_image(tag, function, filename, *args, **kwargs):
    return "UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail."

    buffer, aspect_ratio = function(*args, return_aspect_ratio=True, **kwargs)

    image_file_path = tag.gdocs.add_image_file(buffer, filename)
    buffer.close()

    return image_element(image_file_path, aspect_ratio)


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
