# Generated by Django 3.1.4 on 2021-02-20 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20210220_1759'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_code',
            new_name='order_number',
        ),
    ]
