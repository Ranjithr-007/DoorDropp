# Generated by Django 3.2.3 on 2021-06-10 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0027_alter_orderdelivery_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdelivery',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
