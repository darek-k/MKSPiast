# Generated by Django 3.1.2 on 2020-12-18 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20201217_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='matches',
            field=models.IntegerField(default=0),
        ),
    ]
