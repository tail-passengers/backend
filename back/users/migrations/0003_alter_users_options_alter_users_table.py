# Generated by Django 5.0.2 on 2024-02-14 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_users_profile_image_alter_users_user_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'ordering': ['created_time']},
        ),
        migrations.AlterModelTable(
            name='users',
            table='Users',
        ),
    ]