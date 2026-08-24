import re

from django.shortcuts import get_object_or_404

from api.models import Dataset

# Name a report {spider}_{date} to share it with the publisher's users, and anything else to keep it internal.
# Pelican backend copies a report's name into a report filtered from it, so a filtered report is shared, too.
DATE_SUFFIX = r"_\d{4}-\d{2}-\d{2}$"


def permitted_datasets(user):
    """Return the datasets the user can see: all of them, if staff, or those in their publishers' namespaces."""
    if user.is_staff:
        return Dataset.objects.all()
    # The publishers are in another database, so their spiders are read here, rather than joined in the query.
    spiders = list(user.publishers.values_list("spider", flat=True))
    if not spiders:
        return Dataset.objects.none()
    pattern = "|".join(map(re.escape, spiders))
    return Dataset.objects.filter(name__regex=rf"^({pattern}){DATE_SUFFIX}")


def get_permitted_dataset(user, pk):
    """Return the dataset if the user can see it, and raise ``Http404`` otherwise."""
    return get_object_or_404(permitted_datasets(user), pk=pk)
