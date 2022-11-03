# Generated by Django 3.2.3 on 2021-06-17 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0037_auto_20210617_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
