# Generated by Django 5.0.4 on 2024-05-03 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_app', '0005_article_article_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_date_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
