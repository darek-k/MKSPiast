# Generated by Django 3.1.2 on 2021-03-05 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20210304_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchtest',
            name='away_team_goals',
            field=models.CharField(default='-', max_length=20),
        ),
        migrations.AlterField(
            model_name='matchtest',
            name='home_team_goals',
            field=models.CharField(default='-', max_length=20),
        ),
    ]
