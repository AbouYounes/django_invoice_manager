# Generated by Django 5.0.4 on 2024-05-02 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_app', '0002_article_ttc_article_article_article_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='unit_type',
            field=models.CharField(choices=[('R', 'Hour'), ('P', 'Meter')], max_length=1),
        ),
    ]
