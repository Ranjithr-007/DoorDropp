# Generated by Django 3.2.3 on 2021-06-11 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0031_auto_20210611_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdelivery',
            name='is_delivered',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]