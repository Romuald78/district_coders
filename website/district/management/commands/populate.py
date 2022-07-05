from django.core.management import BaseCommand
from django.db import migrations

from toolbox.migration_tools.debug_data import debug_migration
from toolbox.migration_tools.migration_group import group_migration
from toolbox.migration_tools.migration_inspect_mode import mode_migration
from toolbox.migration_tools.migration_language import language_migration


class Command(BaseCommand):
    def handle(self, *args, **options):
        language_migration()
        mode_migration()
        group_migration()
        debug_migration()
        # migrations.RunPython(language_migration)
        # migrations.RunPython(mode_migration)
        # migrations.RunPython(group_migration)
        # migrations.RunPython(debug_migration)