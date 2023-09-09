from django.contrib import admin
from home.models import Banner

# Register your models here.

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'banner_name',
        'banner_type'
    ]