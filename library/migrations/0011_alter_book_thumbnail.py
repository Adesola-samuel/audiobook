# Generated by Django 3.2.5 on 2021-10-13 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_auto_20211013_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='thumbnail',
            field=models.ImageField(blank=True, help_text='The thumbnail', null=True, upload_to='static/uploads/pdfs'),
        ),
    ]
