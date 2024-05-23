# Generated by Django 5.0.6 on 2024-05-23 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_rename_itinerary_trip_itinerary'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='travelers',
            field=models.ManyToManyField(blank=True, related_name='trip', to='test_app.user'),
        ),
    ]
