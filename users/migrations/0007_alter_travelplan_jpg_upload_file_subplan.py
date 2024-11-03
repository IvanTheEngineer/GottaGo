# Generated by Django 4.2.16 on 2024-10-27 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_travelplan_plan_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelplan',
            name='jpg_upload_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/main_plan_jpgs/'),
        ),
        migrations.CreateModel(
            name='SubPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subplan_name', models.CharField(max_length=100)),
                ('subplan_description', models.TextField()),
                ('jpg_upload_file', models.FileField(blank=True, null=True, upload_to='uploads/sub_plan_jpgs/')),
                ('txt_upload_file', models.FileField(blank=True, null=True, upload_to='uploads/txts/')),
                ('pdf_upload_file', models.FileField(blank=True, null=True, upload_to='uploads/pdfs/')),
                ('travel_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subplans', to='users.travelplan')),
            ],
        ),
    ]
