# Generated by Django 4.2.16 on 2024-11-15 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_travelplan_start_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="travelplan",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]