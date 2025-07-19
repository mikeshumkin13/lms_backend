from django.contrib.auth import get_user_model
from decimal import Decimal
from rest_framework import serializers
from .models import Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "city",
            "avatar",
            "payments",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user


class PublicUserProfileSerializer(serializers.ModelSerializer):
    """Публичная версия профиля (без фамилии, платежей и т.д.)"""

    class Meta:
        model = User
        fields = ["email", "first_name", "city", "avatar"]



class StripePaymentCreateSerializer(serializers.Serializer):
    course = serializers.IntegerField(required=False)
    lesson = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHOD_CHOICES)

    def validate(self, data):
        if not data.get("course") and not data.get("lesson"):
            raise serializers.ValidationError("Нужно указать курс или урок.")
        if data.get("course") and data.get("lesson"):
            raise serializers.ValidationError("Нельзя указывать одновременно курс и урок.")
        return data

    def validate_amount(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError("Сумма должна быть больше нуля.")
        return value

