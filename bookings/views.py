from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Booking
from .serializers import BookingSerializer  # <-- BARIS INI WAJIB ADA AGAR TIDAK NOT DEFINED

# ==========================================
# GOLONGAN USER BIASA (CLIENT-SIDE - FR-07, FR-08, FR-09, FR-10)
# ==========================================

# 1. Menangani Pembuatan dan Daftar Riwayat
class BookingCreateListView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

# 2. Menangani Detail dan Upload Bukti Pembayaran
class BookingDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

# 3. Menangani Logika Pembatalan Pesanan
class BookingCancelView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.status in ['PENDING', 'WAITING_CONFIRMATION']:
            booking.status = 'CANCELLED'
            booking.save()
            return Response({"message": "Pesanan berhasil dibatalkan."}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Pesanan tidak dapat dibatalkan karena sudah diproses oleh admin."}, 
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================
# GOLONGAN SUPER ADMIN (BACK-OFFICE - FR-08 BERSILANG)
# ==========================================

# 4. Menangani daftar semua booking dari seluruh user (Khusus Admin)
class AdminBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser] 
    queryset = Booking.objects.all().order_by('-created_at')

# 5. Menangani persetujuan/penolakan status booking (Khusus Admin)
class AdminBookingStatusUpdateView(generics.UpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]
    queryset = Booking.objects.all()

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        new_status = request.data.get('status')

        if new_status in ['CONFIRMED', 'REJECTED']:
            booking.status = new_status
            booking.save()
            return Response(
                {"message": f"Status pesanan berhasil diperbarui menjadi {new_status}."}, 
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Status tidak valid. Admin hanya bisa mengubah ke CONFIRMED atau REJECTED."}, 
            status=status.HTTP_400_BAD_REQUEST
        )