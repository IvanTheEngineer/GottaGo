from django.contrib import admin
from .models import GroupCode, TravelPlan

@admin.register(GroupCode)
class GroupCodeAdmin(admin.ModelAdmin):
    list_display = ('code',)
    search_fields = ('code',)
    filter_horizontal = ('users',)

admin.site.register(TravelPlan)