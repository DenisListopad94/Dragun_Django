# Generated by Django 4.2.13 on 2024-06-22 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_service', '0011_profile_info_alter_profile_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(unique=True)),
            ],
        ),
    ]