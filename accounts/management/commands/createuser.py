from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create users. No password is set."

    def add_arguments(self, parser):
        parser.add_argument("username", nargs="+", help="the username to create")
        parser.add_argument("--staff", action="store_true", help="create the users as staff and superusers")

    def handle(self, *args, **options):
        user_model = get_user_model()
        for username in options["username"]:
            user = user_model.objects.filter(username=username).first()
            if user is None:
                user_model.objects.create_user(username, is_staff=options["staff"], is_superuser=options["staff"])
            elif options["staff"]:
                user.is_staff = True
                user.is_superuser = True
                user.save(update_fields=["is_staff", "is_superuser"])
