from django.contrib import admin
from .models import TravelPlan

# admin.site.register(TravelPlan)

@admin.register(TravelPlan)
class TravelPlanAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)