# Generated by Django 3.0.7 on 2021-02-07 10:33

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210207_0747'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movement',
            options={'verbose_name': 'Movement', 'verbose_name_plural': 'Movements'},
        ),
        migrations.AddField(
            model_name='session',
            name='goal',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), null=True, size=None),
        ),
        migrations.AddField(
            model_name='session',
            name='start',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), null=True, size=None),
        ),
    ]
