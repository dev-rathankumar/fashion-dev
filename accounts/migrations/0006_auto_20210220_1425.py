# Generated by Django 3.1.4 on 2021-02-20 08:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210109_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address_line_1',
            field=models.CharField(default='Mumbai', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='address_line_2',
            field=models.CharField(blank=True, default='Mumbai', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(default='Mumbai', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.country'),
        ),
        migrations.AddField(
            model_name='customer',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='pin_code',
            field=models.CharField(default='Mumbai', max_length=50),
        ),
        migrations.AddField(
            model_name='customer',
            name='state',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='country', chained_model_field='country', default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.state'),
        ),
    ]