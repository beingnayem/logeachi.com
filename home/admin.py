from django.contrib import admin
from home.models import Newsletter, Queries, Home_Slider, Event, Banner, Feedback, Deal_of_the_day

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
        'email',
        'gender'
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
    
    
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'banner_title',
        'banner_product_category'
    ]
    
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'event_title',
        'event_product_category'
    ]
    
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'feedback_date'
    ]
    
@admin.register(Deal_of_the_day)
class Deal_of_the_dayAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'created_at',
        'deadline'
    ]