# Generated by Django 5.0.1 on 2024-03-09 15:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='Profile_User',
        ),
    ]