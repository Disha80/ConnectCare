# Generated by Django 4.2.17 on 2025-01-29 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_helprequest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='helprequest',
            options={'ordering': ['-created_at']},
        ),
    ]
