# Generated by Django 3.2.5 on 2021-10-24 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0018_alter_book_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='pdf',
            field=models.TextField(blank=True, null=True),
        ),
    ]
