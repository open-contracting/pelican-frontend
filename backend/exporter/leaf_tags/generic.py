import datetime
from typing import Any, Dict, List, Type, Union

from lxml import etree

from exporter.decorators import argument, leaf
from exporter.tag import LeafTag
from exporter.util import LEVELS, MODES, sample_and_format

DATETIME_FORMATS = {
    "datetime": "%Y-%m-%d %H:%M:%S",
    "date": "%Y-%m-%d",
    "time": "%H:%M:%S",
}


def generate_key_leaf_tag(key: str) -> Type[LeafTag]:
    """
    Build a :class:`~exporter.tag.LeafTag` named ``key``, that returns the ``key`` from the context.
    """

    @leaf(key)
    def tag(tag: LeafTag, data: Dict[str, Any]) -> str:
        return str(data[key])

    return tag


def generate_count_leaf_tag(infix: str) -> Type[LeafTag]:
    """
    Build a :class:`~exporter.tag.LeafTag` named ``{infix.lower()}Count`` with a ``level`` argument, that returns the
    ``{level}{infix}Count`` from the context.
    """

    @argument("level", required=True, choices=LEVELS)
    @leaf(f"{infix.lower()}Count")
    def _tag(tag: LeafTag, data: Dict[str, Any]) -> str:
        return str(data[f"{tag.arguments['level']}{infix}Count"])

    return _tag


def generate_sample_leaf_tag(key: str) -> Type[LeafTag]:
    """
    Build a :class:`~exporter.tag.LeafTag` named ``key`` with ``mode`` and ``max`` arguments, that returns a sample of
    the ``key`` from the context.
    """

    @argument("mode", choices=MODES, default="oneLine")
    @argument("max", type=int, nonzero=True)
    @leaf(key)
    def _tag(tag: LeafTag, data: Dict[str, Any]) -> Union[str, List[etree.Element]]:
        return sample_and_format(data[key], tag.arguments)

    return _tag


def generate_timestamp_leaf_tag(key: str, datetime_format: str) -> Type[LeafTag]:
    """
    Build a :class:`~exporter.tag.LeafTag` named ``key`` with a ``mode`` argument, that returns the ``key`` from the
    context in the format specified by ``mode``. The ``key`` value is parsed according to ``datetime_format``.
    """

    @argument("mode", choices=DATETIME_FORMATS, default="datetime")
    @leaf(key)
    def _tag(tag: LeafTag, data: Dict[str, Any]) -> str:
        d = datetime.datetime.strptime(data[key], datetime_format)
        return d.strftime(DATETIME_FORMATS[tag.arguments["mode"]])

    return _tag
