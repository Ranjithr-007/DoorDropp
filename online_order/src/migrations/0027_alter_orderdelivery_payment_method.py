# Generated by Django 3.2.3 on 2021-06-10 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0026_auto_20210607_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdelivery',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='src.paymentmethod'),
        ),
    ]
