# Generated by Django 4.0.4 on 2022-05-16 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('district', '0004_alter_language_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='icon',
            field=models.URLField(),
        ),
    ]