# Generated by Django 3.2.3 on 2021-06-03 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0020_auto_20210601_2339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commonuser',
            old_name='location',
            new_name='landmark',
        ),
    ]
