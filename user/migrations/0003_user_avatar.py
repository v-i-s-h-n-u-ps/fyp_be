# Generated by Django 3.0.5 on 2021-03-29 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210228_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.TextField(default=''),
        ),
    ]
