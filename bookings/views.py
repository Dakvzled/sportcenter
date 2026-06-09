from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer

class BookingCreateListView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    
    # Kunci pintu: WAJIB menyertakan header otorisasi JWT (Bearer Token)
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        # FR-10: Pastikan user HANYA BISA melihat riwayat pesanannya sendiri
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date', '-start_time')