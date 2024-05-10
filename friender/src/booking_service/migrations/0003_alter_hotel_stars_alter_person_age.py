# Generated by Django 5.0.4 on 2024-05-05 09:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_service', '0002_person_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='stars',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='person',
            name='age',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(120), django.core.validators.MinValueValidator(0)]),
        ),
    ]