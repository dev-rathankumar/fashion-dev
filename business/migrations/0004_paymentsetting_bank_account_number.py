# Generated by Django 3.1.4 on 2021-02-26 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_paymentsetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentsetting',
            name='bank_account_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
