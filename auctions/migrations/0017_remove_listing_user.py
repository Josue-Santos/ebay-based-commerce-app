# Generated by Django 3.1.6 on 2021-03-01 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_listing_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='user',
        ),
    ]
