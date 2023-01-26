import random
from collections.abc import Iterable
from typing import Any, Dict, List, Union

from lxml import etree

from exporter.tag import LeafTag

LEVELS = {"coverage", "coverageSet", "coverageEmpty", "quality"}
MODES = {"oneLine", "multipleLines"}


def quote_list(it: Iterable[str]) -> str:
    """
    Wrap each element in single quotation marks and return as a comma-separated string.

    :param it: an iterable
    """
    return ", ".join(f"'{el}'" for el in sorted(it))


def sample_and_format(population, arguments: Dict[str, Any]) -> Union[str, List[etree.Element]]:
    """
    Call :py:func:`random.sample`, bounding the sample size in ``arguments["max"]`` to the population size.

    If ``arguments["mode"]`` is "oneLine", return the sample as a comma-separated string.

    Otherwise, return the sample as a list of paragraphs.
    """
    length = len(population)
    examples = random.sample(population, k=min(length, arguments.get("max", length)))

    if arguments["mode"] == "oneLine":
        return ", ".join(examples)
    return multiple_line_elements(examples)


def multiple_line_elements(it: Iterable[str]) -> List[etree.Element]:
    """
    Wrap each element in a paragraph and return as a list of paragraphs.

    :param it: an iterable
    """
    elements = []
    for el in it:
        element = etree.Element(
            "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p",
            attrib={"{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name": "Standard"},
        )
        element.text = str(el)
        elements.append(element)
    return elements


def image_element(path: str, aspect_ratio: float) -> etree.Element:
    """
    Return an image within a frame.

    :param path: the path to the image within the OpenDocument file
    :param aspect_ratio: the aspect ratio of the image
    """
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


def box_image(tag: LeafTag, function, filename: str, *args, **kwargs) -> etree.Element:
    return "UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail."

    buffer, aspect_ratio = function(*args, return_aspect_ratio=True, **kwargs)

    path = tag.gdocs.add_image_file(buffer, filename)
    buffer.close()

    return image_element(path, aspect_ratio)
