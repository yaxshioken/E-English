
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from account.models import User
from account.serializers import (CheckCodeSerializer, LoginSerializer,
                                 SendCodeSerializer, UserSerializer)
from account.tasks import send_email


class CustomTokenObtainPairView(TokenObtainPairView):
    pass


class CustomTokenRefreshView(TokenRefreshView):
    pass


class SendEmailCodeView(APIView):
    queryset = User.objects.all()
    serializer_class = SendCodeSerializer
    my_tags = [
        "send-code",
    ]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        query = User.objects.filter(email=email)
        if not query.exists():
            User.objects.create(email=email, is_active=False)
        elif query.first().is_active:
            raise ValidationError("Bunday email mavjud!")
        send_email.delay(email)
        return Response(
            f"Send code:<h1>{email}</h1>",
            status=status.HTTP_200_OK,
            content_type="text/html",
        )


class CheckCodeView(APIView):
    serializer_class = CheckCodeSerializer
    my_tags = [
        "check-code",
    ]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    my_tags = [
        "register",
    ]


    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        query = User.objects.filter(email=email)
        if not query.exists():
            raise ValidationError(
                "Bunday foydalanuvchi Topilmadi!!!", code=status.HTTP_400_BAD_REQUEST
            )
        if query.exists() and query.first().password:
            raise ValidationError(
                "Foydalanuvchi ro'yxatdan o'tgan!!!", code=status.HTTP_400_BAD_REQUEST
            )  ##TODO
        if not query and query.is_active == False:
            raise ValidationError(
                "Bunday foydalanuvchi topilmadi!!", code=status.HTTP_400_BAD_REQUEST
            )
        if query.exists() and query.first().is_active == False:
            raise ValidationError(
                f"Emailingizni tasdiqlang : {email}", code=status.HTTP_400_BAD_REQUEST
            )
        password = password.make_password(password)
        query.update(password=password)
        return Response("Register success", status=status.HTTP_200_OK)


class LoginView(APIView):
    serializer_class = LoginSerializer
    my_tags = [
        "login",
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Login Successfully"}, status=status.HTTP_200_OK
            )
