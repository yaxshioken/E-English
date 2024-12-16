import datetime


import jwt
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.models import User
from account.serializers import (CheckCodeSerializer, LoginSerializer,
                                 SendCodeSerializer, UserSerializer)
from config.settings import SECRET_KEY


class SendEmailCodeView(APIView):
    queryset = User.objects.all()
    serializer_class = SendCodeSerializer
    permission_classes = (AllowAny,)
    my_tags = [
        "send-code",
    ]

    @swagger_auto_schema(
        operation_description="Emailga tasdiqlash uchun code yuboradi!!",
        request_body=SendCodeSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"muvaffaqiyatli": f"{request.data.get("email")} ga code yuborildi!!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CheckCodeView(APIView):
    serializer_class = CheckCodeSerializer
    permission_classes = (AllowAny,)
    my_tags = [
        "check-code",
    ]

    @swagger_auto_schema(
        operation_description="Kodni tekshirish uchun ishlatiladi!!!",
        request_body=CheckCodeSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"muvaffaqiyatli": "Email Tasdiqlandi"}, status=status.HTTP_200_OK)



class RegisterView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    my_tags = [
        "register",
    ]

    @swagger_auto_schema(
        operation_description="Yangi user yaratish uchun ishlatiladi!!!",
        request_body=UserSerializer,
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        query = User.objects.filter(email=email)
        if not query.exists():
            raise ValidationError(
                {"xato":"Bunday foydalanuvchi Topilmadi!!!"}, code=status.HTTP_400_BAD_REQUEST
            )

        if not query and query.is_active == False:
            raise ValidationError(
                {"xato":"Bunday foydalanuvchi topilmadi!!"}, code=status.HTTP_400_BAD_REQUEST
            )
        if query.exists() and query.first().is_active == False:
            raise ValidationError(
                {"ma'lumot":f"Emailingizni tasdiqlang : {email}"}, code=status.HTTP_400_BAD_REQUEST
            )
        user=User.objects.get(email=email)

        if user.password:
            raise ValidationError(
                {"xato":"Foydalanuvchi ro'yxatdan o'tgan!!!"}, code=status.HTTP_400_BAD_REQUEST
            )
        password = make_password(password)
        query.update(password=password)
        return Response({"muvaffaqiyatli":"Register success"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    my_tags = [
        "login",
    ]
    @swagger_auto_schema(
        operation_description='Login qilish',
        request_body=LoginSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            raise AuthenticationFailed({"xato":"Bunday emailli foydalanuvchi topilmadi!!!"})

        if not user.check_password(password):
            raise AuthenticationFailed({"xato":"Parol No'to'g'ri!!"})
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            "iat": datetime.datetime.utcnow(),

        }

        response=Response()
        token = jwt.encode(payload,SECRET_KEY, algorithm='HS256')

        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={"jwt":token}
        return response


class LogoutView(APIView):
    my_tags = ['logout',]
    permission_classes = (AllowAny,)
    @swagger_auto_schema(operation_description='Logout',)
    def post(self,request):
        response=Response()
        response.delete_cookie(key='jwt')
        response.data={"muvaffaqiyatli":"Profildan chiqildi!"   }
        return response
class CustomTokenObtainPairView(TokenObtainPairView):
    my_tags = ['token', ]
    permission_classes = (AllowAny,)
    pass


class CustomTokenRefreshView(TokenRefreshView):
    my_tags=['token',]
    permission_classes = (AllowAny,)
    pass

