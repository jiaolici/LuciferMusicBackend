# Generated by Django 2.2.3 on 2020-08-23 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('LuciferMusic', '0007_auto_20200822_1100'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fav',
            unique_together={('user', 'content_type', 'object_id')},
        ),
    ]
