# Generated by Django 5.1.4 on 2024-12-19 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_trip_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]