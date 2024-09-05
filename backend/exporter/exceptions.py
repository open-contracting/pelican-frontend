class PelicanError(Exception):
    """Base class for exceptions from within this project."""


class GoogleDriveError(PelicanError):
    """
    Raised if an error occurs interacting with a Google API.

    :param reason: the error message
    """

    def __init__(self, reason: str):
        self.args = (reason,)
        self.reason = reason

    def __str__(self) -> str:
        return f"Google Drive Error: {self.reason}"


class TagError(PelicanError):
    """
    Base class for exceptions related to tags.

    :param reason: the error message
    :param full_tag: the tag as extracted from the template
    :param template_id: the file ID of the template in Google Docs
    """

    def __init__(self, reason: str, full_tag: str | None = None, template_id: str | None = None):
        self.args = (reason,)
        self.reason = reason
        self.full_tag = full_tag
        self.template_id = template_id

    def fill(self, full_tag: str, template_id: str) -> "TagError":
        """
        Add metadata to the exception to assist in debugging.

        :param full_tag: the tag as extracted from the template
        :param template_id: the file ID of the template in Google Docs
        """
        if self.full_tag is None:
            self.full_tag = full_tag
        if self.template_id is None:
            self.template_id = template_id
        return self

    def as_dict(self) -> dict[str, str | None]:
        """
        Return the exception as a dictionary (e.g. to serialize as JSON for the browser).
        """
        return {
            "reason": self.reason,
            "full_tag": self.full_tag,
            "template_id": self.template_id,
        }


class TagSyntaxError(TagError):
    """Raised if a tag is malformed."""


class UnknownTagError(TagError):
    """Raised if a tag's name is unrecognized."""


class TagArgumentError(TagError):
    """Raised if a tag's argument is invalid."""


class MissingArgumentError(TagError):
    """Raised if a tag's argument is missing."""


class CheckNotComputedError(PelicanError):
    """Raised if a check cannot be computed. The error message should be the check's name."""
