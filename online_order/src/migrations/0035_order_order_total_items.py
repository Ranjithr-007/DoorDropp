# Generated by Django 3.2.3 on 2021-06-16 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0034_paymentmethod_is_upi'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_total_items',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
