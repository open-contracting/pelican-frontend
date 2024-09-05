import random
from typing import Any

from lxml import etree

LEVELS = {"coverage", "coverageSet", "coverageEmpty", "quality"}
MODES = {"oneLine", "multipleLines"}


def quote_list(it: dict[str, Any] | list[str] | set[str]) -> str:
    """
    Wrap each element in single quotation marks and return as a comma-separated string.

    :param it: an iterable
    """
    return ", ".join(f"'{el}'" for el in sorted(it))


def sample_and_format(population, arguments: dict[str, Any]) -> str | list[etree._Element]:
    """
    Call :py:func:`random.sample`, bounding the sample size in ``arguments["max"]`` to the population size.

    If ``arguments["mode"]`` is "oneLine", return the sample as a comma-separated string.

    Otherwise, return the sample as a paragraph list.

    :param population: the population to sample
    :param arguments: the tag's arguments
    """
    length = len(population)
    examples = random.sample(population, k=min(length, arguments.get("max", length)))

    if arguments["mode"] == "oneLine":
        return ", ".join(examples)

    elements = []
    for example in examples:
        element = etree.Element(
            "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p",
            attrib={"{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name": "Standard"},
        )
        element.text = str(example)
        elements.append(element)
    return elements


def box_image(tag, function, filename: str, *args, **kwargs) -> etree._Element:
    """
    Add an image to the OpenDocument file and return an image within a frame.
    """
    buffer, aspect_ratio = function(*args, **kwargs)

    path = tag.gdocs.add_image_file(buffer, filename)
    buffer.close()

    frame = etree.Element(
        "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}frame",
        attrib={
            # '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name': 'fr1',
            "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name": path,
            "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}anchor-type": "as-char",
            "{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width": "6.0cm",
            "{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height": "%fcm" % (6 * aspect_ratio),
            "{urn:oasis:names:tc:opendocument:xmlns:style:1.0}rel-width": "100%",
            "{urn:oasis:names:tc:opendocument:xmlns:style:1.0}rel-height": "scale",
            "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}z-index": "0",
        },
    )
    frame.append(
        etree.Element(
            "{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}image",
            attrib={
                "{http://www.w3.org/1999/xlink}href": path,
                "{http://www.w3.org/1999/xlink}type": "simple",
                "{http://www.w3.org/1999/xlink}show": "embed",
                "{http://www.w3.org/1999/xlink}actuate": "onLoad",
                "{urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0}mime-type": "image/png",
            },
        )
    )
    return frame
