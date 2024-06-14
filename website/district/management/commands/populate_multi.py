from django.core.management import BaseCommand

from toolbox.migration_tools.debug_data import debug_migration

class Command(BaseCommand):
    def handle(self, *args, **options):
        debug_migration()
