# Generated by Django 4.1.7 on 2023-03-31 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_rename_fcm_id_users_fcm_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='providers',
            name='service_category',
        ),
        migrations.RemoveField(
            model_name='servicecategories',
            name='parent_category',
        ),
        migrations.AddField(
            model_name='providers',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='providers',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='providers',
            name='service_range',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='ServiceSubcategories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('parent_service_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_categories', to='login.servicecategories')),
                ('service_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='login.servicecategories')),
            ],
            options={
                'db_table': 'service_subcategories',
            },
        ),
        migrations.CreateModel(
            name='ProviderServiceCategories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.providers')),
                ('service_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.servicecategories')),
            ],
            options={
                'db_table': 'provider_categories',
                'unique_together': {('provider', 'service_category')},
            },
        ),
    ]
