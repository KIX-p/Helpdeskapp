# Generated by Django 4.2.7 on 2023-12-11 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdeskapp', '0004_alter_ticket_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['-created_at'], 'permissions': [('can_change_status', 'Can change status'), ('can_change_priority', 'Can change priority'), ('can_change_request_type', 'Can change request type'), ('can_change_assigned_to', 'Can change assigned to')]},
        ),
    ]
