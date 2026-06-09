from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def api_root_view(request):
    return JsonResponse({
        "project": "Sport Center Solo Booking System (SCSBS)",
        "status": "API is running securely",
        "available_endpoints": {
            "admin_panel": "/admin/",
            "fields_catalog": "/api/fields/",
            "user_register": "/api/users/register/",
            "auth_login": "/api/login/",
            "bookings": "/api/bookings/"
        }
    })

urlpatterns = [
    path('', api_root_view, name='api-root'), 
    path('admin/', admin.site.urls),
    
    # Modul Utama
    path('api/fields/', include('fields.urls')),
    path('api/users/', include('users.urls')),
    
    # --- RUTE BARU UNTUK PEMESANAN ---
    path('api/bookings/', include('bookings.urls')),
    # ---------------------------------
    
    # JWT Auth
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)