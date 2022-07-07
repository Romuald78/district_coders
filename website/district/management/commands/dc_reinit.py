from django.core import management
from django.core.management.commands.migrate import Command as CoreMigrateCommand
from django.db import migrations

class Command(CoreMigrateCommand):
    def handle(self, *args, **options):
        # Call CLEAN command
#        management.call_command('clean')
        management.call_command('flush', '--noinput')

        # perform normal migration
        super().handle(*args, **options)

        # Populate with default information
        management.call_command('populate_admin')

        # Populate with default information
        management.call_command('populate_default')
