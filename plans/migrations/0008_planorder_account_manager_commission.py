# Generated by Django 3.1.4 on 2021-04-17 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0007_planorder_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='planorder',
            name='account_manager_commission',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]