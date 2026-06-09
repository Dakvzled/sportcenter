from django.urls import path
from .views import BookingCreateListView

urlpatterns = [
    path('', BookingCreateListView.as_view(), name='booking-list-create'),
]