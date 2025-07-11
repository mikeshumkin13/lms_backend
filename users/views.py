from django.contrib.auth import get_user_model
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Payment
from .serializers import (
    PaymentSerializer,
    UserProfileSerializer,
    PublicUserProfileSerializer,
    UserRegisterSerializer,
)

User = get_user_model()


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.request.query_params.get("id")
        if user_id:
            return User.objects.get(pk=user_id)
        return self.request.user

    def get_serializer_class(self):
        if self.request.user.pk == self.get_object().pk:
            return UserProfileSerializer  # Полный доступ (с платежами и др.)
        return PublicUserProfileSerializer  # Ограниченный доступ


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []
