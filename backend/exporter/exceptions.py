class PelicanError(Exception):
    """Base class for exceptions from within this project"""


class GoogleDriveError(PelicanError):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return f"Google Drive Error: {self.reason}"


class TagError(PelicanError):
    """Base class for exceptions related to tags."""

    def __init__(self, reason, full_tag=None, template_id=None):
        self.args = (reason,)
        self.reason = reason
        self.full_tag = full_tag
        self.template_id = template_id

    def fill(self, full_tag, template_id):
        if self.full_tag is None:
            self.full_tag = full_tag
        if self.template_id is None:
            self.template_id = template_id
        return self

    def as_dict(self):
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
