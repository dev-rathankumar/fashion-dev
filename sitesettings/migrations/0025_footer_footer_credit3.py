# Generated by Django 3.1.4 on 2021-06-09 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitesettings', '0024_auto_20210608_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='footer',
            name='footer_credit3',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]