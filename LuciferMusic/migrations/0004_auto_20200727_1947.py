# Generated by Django 2.2.3 on 2020-07-27 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LuciferMusic', '0003_auto_20200727_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
