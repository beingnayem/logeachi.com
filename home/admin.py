from django.contrib import admin
from home.models import Banner, Subscribers

# Register your models here.

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'banner_name',
        'banner_type'
    ]
    
@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'email',
    ]