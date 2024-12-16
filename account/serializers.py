from redis import Redis
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from account.models import User
from account.tasks import send_email
class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate(self, attrs):
        email = attrs.get("email")

        query = User.objects.filter(email=email)
        if not query.exists():
            User.objects.create(email=email, is_active=False)
        elif query.first().is_active:
            raise ValidationError({"error":"Bunday email mavjud!"})
        send_email.delay(email)
        return attrs


class CheckCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        r=Redis(decode_responses=True)
        verify = r.get('code')
        try:
            user = User.objects.filter(email=email)
            if code != verify:
                raise ValidationError({"xato":'Tasdiqlash kodi xato!!!'})
            user.update(is_active=True)
        except User.DoesNotExist:
            raise ValidationError({"xato":"Bunday emailli foydalanuvchi topilmadi!!!"})
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        read_only_fields = ("id",)
        write_only_fields = ("password",)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

