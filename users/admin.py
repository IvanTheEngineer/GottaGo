from django.contrib import admin
from .models import TravelPlan, FileMetadata

@admin.register(TravelPlan)
class TravelPlanAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)

@admin.register(FileMetadata)
class FileMetadataAdmin(admin.ModelAdmin):
    list_display = ('file_title', 'content_type', 'object_id', 'upload_timestamp')
    search_fields = ('file_title', 'description', 'keywords')