# Generated by Django 4.0.1 on 2022-02-10 09:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
