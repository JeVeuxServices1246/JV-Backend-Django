# Generated by Django 4.1.7 on 2023-04-13 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_useraddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
