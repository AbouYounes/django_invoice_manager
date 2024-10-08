# Generated by Django 5.0.6 on 2024-07-24 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_app', '0027_invoice_invoice_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_date_time',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='last_updated_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
