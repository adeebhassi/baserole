# Generated by Django 5.1.3 on 2024-11-22 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_active_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
    ]
