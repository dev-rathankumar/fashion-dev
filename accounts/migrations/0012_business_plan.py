# Generated by Django 3.1.4 on 2021-04-16 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_remove_plan_business'),
        ('accounts', '0011_regionalmanager_commission_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='plan',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='plans.plan'),
        ),
    ]