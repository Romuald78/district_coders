from django.core import management
from django.core.management import BaseCommand
from django.db import migrations


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Load DB config
        fp = open('./config/secure/mysql_db.cnf', 'r')
        content = fp.readlines()
        fp.close()
        db_name = None
        for row in content:
            row = row.replace('\n', '')
            row = row.replace('\r', '')
            row = [x.strip() for x in row.split("=")]
            if row[0] == "database":
                db_name = row[1]
        # Remove database if it exists
        if db_name is not None:
            print("database drop ...")
            migrations.RunSQL(f"DROP DATABASE `{db_name}`")
        # Recreate database
        print("database creation ...")
        migrations.RunSQL(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
