from django.contrib import admin
from .models import TravelPlan, FileMetadata, Invite, Destination

@admin.register(TravelPlan)
class TravelPlanAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)

@admin.register(FileMetadata)
class FileMetadataAdmin(admin.ModelAdmin):
    list_display = ('file_title', 'content_type', 'object_id', 'upload_timestamp')
    search_fields = ('file_title', 'description', 'keywords')

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
   list_display = ('travel_plan', 'requested_by', 'requested_to')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('destination_description', 'jpg_upload_file', 'txt_upload_file', 'pdf_upload_file', 'location_name', 'location_address', 'latitude', 'longitude')
