from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from lessons.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Unseeding initial data...")

        try:
            app_models = apps.get_app_config("lessons").get_models()

            for model in app_models:
                if model.__name__ == "User":
                    User.objects.filter(is_superuser=False).delete()
                else:
                    model.objects.all().delete()
        except:
            raise CommandError("Unable to unseed initial data.")

        print("Initial data unseeded.")