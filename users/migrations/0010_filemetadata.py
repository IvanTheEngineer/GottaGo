# Generated by Django 4.2.16 on 2024-11-02 05:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0009_destination_user_destination_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_title', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(255)])),
                ('upload_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField()),
                ('keywords', models.CharField(help_text='Comma-separated keywords', max_length=500)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'indexes': [models.Index(fields=['content_type', 'object_id'], name='users_filem_content_6e79ed_idx')],
            },
        ),
    ]