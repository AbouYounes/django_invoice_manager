# Generated by Django 5.0.4 on 2024-05-23 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_app', '0013_alter_entrepreneur_age'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrepreneur',
            options={'verbose_name': 'Entrepreneur', 'verbose_name_plural': 'Entrepreneurs'},
        ),
    ]
