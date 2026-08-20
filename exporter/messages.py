import json
import re
from typing import Any

from django.conf import settings

DEFAULT_LANGUAGE = "en"
MESSAGES: dict[str, Any] = {
    path.stem: json.loads(path.read_text())
    for path in (settings.BASE_DIR / "frontend" / "src" / "messages").glob("*.json")
}

SUBSTITUTIONS = {"</p>": "\n\n", "<li>": "- ", "</li>": "\n", "</ul>": "\n", "{'$'}": "$"}
DISCARDED_TAGS = re.compile(r"</?(?:b|code|i|p|ul)>")


def text(message: str) -> str:
    """Convert the HTML message to plain text."""
    for markup, replacement in SUBSTITUTIONS.items():
        message = message.replace(markup, replacement)
    return re.sub(r"\n{3,}", "\n\n", DISCARDED_TAGS.sub("", message)).strip()


def message(language: str, *keys: str) -> str:
    """Return the message as plain text in the requested language, falling back to English, then to the keys."""
    for code in (language, DEFAULT_LANGUAGE):
        value = MESSAGES.get(code, {})
        for key in keys:
            if key not in value:
                break
            value = value[key]
        else:
            return text(value)

    return ".".join(keys)
