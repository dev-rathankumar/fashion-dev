# Generated by Django 3.1.4 on 2021-07-11 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitesettings', '0032_directdepositemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='directdepositemail',
            name='is_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
