# Generated by Django 2.0.2 on 2018-02-18 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(verbose_name='博客内容'),
        ),
    ]
