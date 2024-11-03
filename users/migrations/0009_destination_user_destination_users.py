# Generated by Django 4.2.16 on 2024-10-31 04:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0008_destination_remove_travelplan_pdf_upload_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='destination',
            name='users',
            field=models.ManyToManyField(related_name='destinations', to=settings.AUTH_USER_MODEL),
        ),
    ]