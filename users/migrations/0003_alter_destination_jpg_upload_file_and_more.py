# Generated by Django 4.2.16 on 2024-12-26 00:53

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_destination_latitude_destination_location_address_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="destination",
            name="jpg_upload_file",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="uploads/destinations_jpgs/",
                validators=[users.models.validate_image_extension],
            ),
        ),
        migrations.AlterField(
            model_name="travelplan",
            name="jpg_upload_file",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="uploads/main_plan_jpgs/",
                validators=[users.models.validate_image_extension],
            ),
        ),
    ]