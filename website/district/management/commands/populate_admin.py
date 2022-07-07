from django.core.management import BaseCommand

from toolbox.migration_tools.debug_data import debug_migration, createAdmin
from toolbox.migration_tools.migration_group import group_migration
from toolbox.migration_tools.migration_inspect_mode import mode_migration
from toolbox.migration_tools.migration_language import language_migration


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Create default admin/admin
         createAdmin()

