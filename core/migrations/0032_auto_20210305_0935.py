# Generated by Django 3.1.2 on 2021-03-05 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20210305_0932'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matchtest',
            options={'ordering': ['date']},
        ),
    ]
