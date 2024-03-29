# Generated by Django 3.0.7 on 2021-02-17 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_session_is_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalhome',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='globalposition',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='localposition',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='localvelocity',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='movement',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
