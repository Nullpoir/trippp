# Generated by Django 2.1.1 on 2018-10-15 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabilog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='src',
            field=models.ImageField(upload_to='', verbose_name='画像'),
        ),
    ]
