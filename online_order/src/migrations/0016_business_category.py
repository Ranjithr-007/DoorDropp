# Generated by Django 3.2.3 on 2021-05-27 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0015_paymentmethod_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='src.storecategory'),
        ),
    ]
