from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from account.models import User


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CheckCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        with open("code.txt", "r") as f:
            verify = f.read()
            f.close()
        try:
            user = User.objects.get(email=email)
            if code != verify:
                raise ValidationError('Verification code is invalid!!!')
            user.update(is_active=True)
        except User.DoesNotExist:
            raise ValidationError("Bunday emailli foydalanuvchi topilmadi!!!")
        return attrs
        # if verify != code:
        #     raise ValidationError(
        #         "Verification code is not correct", code=status.HTTP_400_BAD_REQUEST
        #     )
        # User.objects.filter(email=email).update(is_active=True)
        # return attrs


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
