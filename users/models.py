from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.core.validators import MinLengthValidator, MaxLengthValidator
import os


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
    # txt_upload_file = models.FileField(upload_to='uploads/txts/', blank=True, null=True)
    # pdf_upload_file = models.FileField(upload_to='uploads/pdfs/', blank=True, null=True)
    primary_group_code = models.CharField(max_length=100)


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

    # def __str__(self):
    #     return self.plan_name
