# Generated by Django 2.2.3 on 2020-07-27 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LuciferMusic', '0005_auto_20200727_2009'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='song',
            unique_together={('name', 'album')},
        ),
    ]