# Generated by Django 3.2.3 on 2021-06-03 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0021_rename_location_commonuser_landmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='price',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
