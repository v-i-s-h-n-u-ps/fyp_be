# Generated by Django 3.0.5 on 2021-02-28 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_studentcategory_studentdetails'),
        ('projects', '0002_auto_20210228_1200'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProjectParticipants',
            new_name='ProjectParticipant',
        ),
    ]