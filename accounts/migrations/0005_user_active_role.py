# Generated by Django 5.1.3 on 2024-11-22 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active_role',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
