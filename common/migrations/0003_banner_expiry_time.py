# Generated by Django 4.1.7 on 2023-04-19 17:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_banner_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='expiry_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 20, 22, 40, 7, 200759)),
        ),
    ]
