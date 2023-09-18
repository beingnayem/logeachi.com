from django.contrib import admin
from home.models import Banner, Newsletter, Queries

# Register your models here.

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'banner_name',
        'banner_type'
    ]
    
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'email'
    ]
    
@admin.register(Queries)
class QueriesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'email',
        'subject',
        'query_date',
        'query_status'
    ]