# Generated by Django 3.1.4 on 2021-02-19 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_auto_20210120_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
