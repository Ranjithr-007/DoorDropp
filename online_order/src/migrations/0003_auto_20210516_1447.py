# Generated by Django 3.2.3 on 2021-05-16 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0002_auto_20210515_2025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business',
            old_name='contact_number',
            new_name='secondary_mobile',
        ),
        migrations.RemoveField(
            model_name='commonuser',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='deliveryagent',
            name='mobile',
        ),
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]