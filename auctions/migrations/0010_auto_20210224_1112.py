# Generated by Django 3.1.6 on 2021-02-24 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210222_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
