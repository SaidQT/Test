# Generated by Django 5.0.6 on 2024-05-23 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='Itinerary',
            new_name='itinerary',
        ),
    ]
