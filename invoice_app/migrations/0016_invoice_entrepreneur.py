# Generated by Django 5.0.4 on 2024-05-23 18:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_app', '0015_alter_invoice_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='entrepreneur',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='invoice_app.entrepreneur'),
            preserve_default=False,
        ),
    ]
