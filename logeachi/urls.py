from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = 'LOGEACHI'
admin.site.site_title = 'LOGEACHI ADMIN'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin-panel/', include('adminpanel.urls')),
    path('cart/', include('cart.urls')),
    path('blog/', include('blog.urls')),
    path('customer/', include('customer.urls')),
    path('order', include('order.urls')),
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
