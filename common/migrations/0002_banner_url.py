# Generated by Django 4.1.7 on 2023-04-19 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
