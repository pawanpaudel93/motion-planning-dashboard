# Generated by Django 3.0.7 on 2021-02-09 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210207_1033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='globalhome',
            options={'get_latest_by': 'id', 'verbose_name': 'Global Home', 'verbose_name_plural': 'Global Home'},
        ),
        migrations.AlterModelOptions(
            name='globalposition',
            options={'get_latest_by': 'id', 'verbose_name': 'Global Position', 'verbose_name_plural': 'Global Positions'},
        ),
        migrations.AlterModelOptions(
            name='localposition',
            options={'get_latest_by': 'id', 'verbose_name': 'Local Position', 'verbose_name_plural': 'Local Positions'},
        ),
        migrations.AlterModelOptions(
            name='localvelocity',
            options={'get_latest_by': 'id', 'verbose_name': 'Local Velocity', 'verbose_name_plural': 'Local Velocities'},
        ),
        migrations.AlterModelOptions(
            name='movement',
            options={'get_latest_by': 'id', 'verbose_name': 'Movement', 'verbose_name_plural': 'Movements'},
        ),
    ]