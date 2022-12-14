# Generated by Django 4.0.6 on 2022-08-02 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocksmodel',
            name='market_cap',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='stocksmodel',
            name='pe_ratio',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='stocksmodel',
            name='volume',
            field=models.IntegerField(null=True),
        ),
    ]
