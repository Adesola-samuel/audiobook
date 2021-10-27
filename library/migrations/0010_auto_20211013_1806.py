# Generated by Django 3.2.5 on 2021-10-13 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_alter_book_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book',
            field=models.FileField(help_text='Upload a pdf document.', upload_to='static/uploads/pdfs', verbose_name='E-book'),
        ),
        migrations.AlterField(
            model_name='record',
            name='voice_record',
            field=models.FileField(upload_to='stati/records'),
        ),
    ]
