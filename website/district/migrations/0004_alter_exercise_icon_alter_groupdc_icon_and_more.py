# Generated by Django 4.0.4 on 2022-06-10 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('district', '0003_alter_userdc_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='icon',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='groupdc',
            name='icon',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='inspectormode',
            name='icon',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='language',
            name='icon',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='testdc',
            name='icon',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='userdc',
            name='icon',
            field=models.TextField(blank=True),
        ),
    ]