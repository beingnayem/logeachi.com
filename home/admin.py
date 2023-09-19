from django.contrib import admin
from home.models import Newsletter, Queries, Home_Slider

# Register your models here.

@admin.register(Home_Slider)
class Home_SliderAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'slider_offer'
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