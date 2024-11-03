from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.core.validators import MinLengthValidator, MaxLengthValidator
import os
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class FileMetadata(models.Model):
    """
    Model to store metadata for uploaded files
    """
    file_title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(1), MaxLengthValidator(255)]
    )
    upload_timestamp = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    keywords = models.CharField(max_length=500, help_text="Comma-separated keywords")
    
    # Generic foreign key to associate with any file field
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return self.file_title

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class TravelPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='plans')
    plan_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(1), MaxLengthValidator(100)]
    )
    group_size = models.IntegerField()
    trip_description = models.TextField()
    jpg_upload_file = models.FileField(upload_to='uploads/main_plan_jpgs/', blank=True, null=True)
    txt_upload_file = models.FileField(upload_to='uploads/txts/', blank=True, null=True)
    pdf_upload_file = models.FileField(upload_to='uploads/pdfs/', blank=True, null=True)
    primary_group_code = models.CharField(max_length=100)

    jpg_metadata = GenericRelation(FileMetadata, related_query_name='travel_plan_jpg')
    txt_metadata = GenericRelation(FileMetadata, related_query_name='travel_plan_txt')
    pdf_metadata = GenericRelation(FileMetadata, related_query_name='travel_plan_pdf')


class Destination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    users = models.ManyToManyField(User, related_name='destinations')
    travel_plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='destinations')
    destination_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(1), MaxLengthValidator(100)]
    )
    destination_description = models.TextField()
    jpg_upload_file = models.FileField(upload_to='uploads/destinations_jpgs/', blank=True, null=True)
    txt_upload_file = models.FileField(upload_to='uploads/destinations_txts/', blank=True, null=True)
    pdf_upload_file = models.FileField(upload_to='uploads/destination_pdfs/', blank=True, null=True)

    # Add GenericRelation for metadata
    jpg_metadata = GenericRelation(FileMetadata, related_query_name='destination_jpg')
    txt_metadata = GenericRelation(FileMetadata, related_query_name='destination_txt')
    pdf_metadata = GenericRelation(FileMetadata, related_query_name='destination_pdf')

    # def __str__(self):
    #     return self.plan_name

