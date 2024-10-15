# Generated by Django 4.2.16 on 2024-10-14 23:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GroupCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=64, unique=True)),
                (
                    "users",
                    models.ManyToManyField(
                        related_name="group_codes", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TravelPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("plan_name", models.CharField(max_length=100)),
                ("group_size", models.IntegerField()),
                ("trip_description", models.TextField()),
                (
                    "jpg_upload_file",
                    models.FileField(blank=True, null=True, upload_to="uploads/jpgs/"),
                ),
                (
                    "txt_upload_file",
                    models.FileField(blank=True, null=True, upload_to="uploads/txts/"),
                ),
                (
                    "pdf_upload_file",
                    models.FileField(blank=True, null=True, upload_to="uploads/pdfs/"),
                ),
                (
                    "primary_group_code",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="plans",
                        to="users.groupcode",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]