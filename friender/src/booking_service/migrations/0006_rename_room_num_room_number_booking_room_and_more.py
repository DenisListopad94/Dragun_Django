# Generated by Django 5.0.4 on 2024-05-19 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_service', '0005_hotelowner_alter_room_type_guest_first_name_idx_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='room_num',
            new_name='number',
        ),
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='booking_service.room'),
        ),
        migrations.AddField(
            model_name='room',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
    ]
