# Generated by Django 5.0.4 on 2024-05-03 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_app', '0007_rename_article_date_time_article_article_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_date',
            field=models.DateField(),
        ),
    ]
