# Generated by Django 3.1.4 on 2021-10-03 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20211003_0758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdf',
            name='slug',
        ),
    ]