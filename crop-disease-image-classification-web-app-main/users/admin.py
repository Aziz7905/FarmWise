from django.contrib import admin
from .models import FarmerProfile
from .models import FarmerProfile, FarmerPost

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'farm_name', 'location', 'contact_number')
    search_fields = ('user__username', 'farm_name', 'location')

@admin.register(FarmerPost)
class FarmerPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
    search_fields = ('title', 'author__user__username')
    list_filter = ('date_posted',)