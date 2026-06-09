from django.urls import path
from .views import (
    BookingCreateListView, 
    BookingDetailUpdateView, 
    BookingCancelView,
    AdminBookingListView,         # <-- Tambahkan import ini
    AdminBookingStatusUpdateView  # <-- Tambahkan import ini
)

urlpatterns = [
    # Rute Client-Side (User Biasa)
    path('', BookingCreateListView.as_view(), name='booking-list-create'),
    path('<int:pk>/', BookingDetailUpdateView.as_view(), name='booking-detail-update'),
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
    
    # --- RUTE BARU BACK-OFFICE (KHUSUS ADMIN) ---
    path('admin/all/', AdminBookingListView.as_view(), name='admin-booking-list'),
    path('admin/<int:pk>/status/', AdminBookingStatusUpdateView.as_view(), name='admin-booking-status-update'),
]