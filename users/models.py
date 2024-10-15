from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin
import os


class GroupCode(models.Model):
    code = models.CharField(max_length=64, unique=True)
    users = models.ManyToManyField(User, related_name='group_codes')
    def __str__(self):
        return self.code
    
class TravelPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    group_size = models.IntegerField()
    trip_description = models.TextField()
    jpg_upload_file = models.FileField(upload_to='uploads/jpgs/', blank=True, null=True)
    txt_upload_file = models.FileField(upload_to='uploads/txts/', blank=True, null=True)
    pdf_upload_file = models.FileField(upload_to='uploads/pdfs/', blank=True, null=True)
    primary_group_code = models.ForeignKey(GroupCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='plans')

    def __str__(self):
        return self.plan_name




