# Generated by Django 5.1.4 on 2024-12-19 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_trip_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='routeitem',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='routeitem',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='routeitem',
            name='category',
        ),
        migrations.RemoveField(
            model_name='routeitem',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='routeitem',
            name='price',
        ),
        migrations.RemoveField(
            model_name='routeitem',
            name='trip',
        ),
        migrations.RemoveField(
            model_name='routeitem',
            name='url',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='is_active',
        ),
    ]
