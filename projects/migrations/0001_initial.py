# Generated by Django 3.0.5 on 2021-02-28 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resources', '0002_category_type_university'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('isComplete', models.BooleanField(default=False)),
                ('isDeferred', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('members', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTask',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('task', models.TextField()),
                ('dueDate', models.DateField()),
                ('isComplete', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resources.Type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectParticipants',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('isLeader', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
    ]
