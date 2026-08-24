from django.contrib.auth.models import User
from django.db import connections
from django.test import TestCase, override_settings

from accounts.models import Publisher
from api.models import (
    DataItem,
    Dataset,
    DatasetFilter,
    DatasetLevelCheck,
    FieldLevelCheck,
    FieldLevelCheckExamples,
    ProgressMonitorDataset,
    Report,
    ResourceLevelCheck,
    ResourceLevelCheckExamples,
    TimeVarianceLevelCheck,
)


@override_settings(TRUST_REMOTE_USER=True)
class PelicanTestCase(TestCase):
    databases = {"default", "pelican_backend"}
    unmanaged = {
        DataItem,
        Dataset,
        DatasetFilter,
        DatasetLevelCheck,
        FieldLevelCheck,
        FieldLevelCheckExamples,
        ProgressMonitorDataset,
        Report,
        ResourceLevelCheck,
        ResourceLevelCheckExamples,
        TimeVarianceLevelCheck,
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connections["pelican_backend"].schema_editor() as schema_editor:
            for model in cls.unmanaged:
                schema_editor.create_model(model)

    @classmethod
    def tearDownClass(cls):
        with connections["pelican_backend"].schema_editor() as schema_editor:
            for model in cls.unmanaged:
                schema_editor.delete_model(model)
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.user = self.sign_in("staff", is_staff=True)

    def sign_in(self, username, *, is_staff=False, spiders=()):
        """Create the user, with their publishers, and sign in as the user."""
        user = User.objects.create_user(username, is_staff=is_staff)
        for spider in spiders:
            Publisher.objects.create(name=spider.title(), spider=spider).users.add(user)
        self.sign_in_as(username)
        return user

    def sign_in_as(self, username):
        """Sign in as the user, who needn't exist."""
        self.client.defaults["HTTP_X_REMOTE_USER"] = username

    def sign_out(self):
        """Sign out, leaving the request unauthenticated."""
        del self.client.defaults["HTTP_X_REMOTE_USER"]

    def create(self, model, **kwargs):
        obj = model(**kwargs)
        obj.full_clean()
        obj.save()
        return obj
