from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from account.models import User


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CheckCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        read_only_fields = ("id",)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Bunday emailli foydalanuvchi topilmadi!!!")

        if not user.check_password(password):
            raise ValidationError("Parol No'to'g'ri!!")

        return attrs
