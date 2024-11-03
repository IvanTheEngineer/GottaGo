# Generated by Django 4.2.16 on 2024-11-03 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_filemetadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelplan',
            name='pdf_upload_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/pdfs/'),
        ),
        migrations.AddField(
            model_name='travelplan',
            name='txt_upload_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/txts/'),
        ),
    ]
