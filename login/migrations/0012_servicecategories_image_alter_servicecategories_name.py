# Generated by Django 4.1.7 on 2023-04-18 06:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_alter_useraddress_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecategories',
            name='image',
            field=models.CharField(default=datetime.datetime(2023, 4, 18, 6, 32, 50, 88291, tzinfo=datetime.timezone.utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='servicecategories',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
