# Generated by Django 2.1.1 on 2018-11-04 06:44

import datetime
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tabilog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now)),
                ('author', models.CharField(max_length=100)),
                ('user_pk', models.IntegerField()),
                ('thambnail', models.ImageField(upload_to='thambnail/')),
                ('body', tinymce.models.HTMLField(verbose_name='content')),
                ('content', tinymce.models.HTMLField(verbose_name='content')),
            ],
        ),
    ]
