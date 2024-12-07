
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from account.serializers import CheckCodeSerializer, LoginSerializer, SendCodeSerializer, UserSerializer
from account.tasks import send_email



class SendEmailCodeView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SendCodeSerializer
    my_tags = ['send-code', ]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        query = User.objects.filter(email=email)
        if not query.exists():
            User.objects.create(email=email, is_active=False)
        elif query.first().is_active:
            raise ValidationError("Bunday email mavjud!", status=status.HTTP_400_BAD_REQUEST)
        send_email.delay(email)
        return Response(f"Send code:<h1>{email}</h1>", status=status.HTTP_200_OK, content_type='text/html')


class CheckCodeView(CreateAPIView):
    serializer_class = CheckCodeSerializer
    my_tags = ['check-code', ]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        with open('code.txt', 'r') as f:
            verify = f.read()
            f.close()
        if verify != code:
            raise ValidationError('Verification code is not correct', code=status.HTTP_400_BAD_REQUEST)
        User.objects.filter(email=email).update(is_active=True)
        return Response("Check code is success", status=status.HTTP_200_OK)

class RegisterView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    my_tags = ['register', ]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        query = User.objects.filter(email=email)
        if not query.exists():
            raise ValidationError("Bunday foydalanuvchi Topilmadi!!!", code=status.HTTP_400_BAD_REQUEST)
        if  query.exists() and query.first().password:
            raise ValidationError("Foydalanuvchi ro'yxatdan o'tgan!!!", code=status.HTTP_400_BAD_REQUEST)##TODO
        if not query and query.is_active == False:
            raise ValidationError('Bunday foydalanuvchi topilmadi!!', code=status.HTTP_400_BAD_REQUEST)
        if query.exists() and query.first().is_active == False:
            raise ValidationError(f'Emailingizni tasdiqlang : {email}', code=status.HTTP_400_BAD_REQUEST)
        password=password.make_password(password)
        query.update(password=password)
        return Response("Register success", status=status.HTTP_200_OK)

class LoginView(CreateAPIView):
    serializer_class = LoginSerializer
    my_tags = ['login', ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"message": "Login Successfully"}, status=status.HTTP_200_OK)


# from django.shortcuts import render, get_object_or_404
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from account.serializers import UserSerializer
#
# """
# CRUD
# Create
# Read
# Update- >   PUT -> obyekt yaratish uchun kerak boladigan hamma fiedlar berilishi kerak.
#             PATCH -> ozgartirilishi kerak bolgan fieldlar berilsa boldi.
# Delete
# """
#
#
# class PollsView(APIView):
#     def get(self, request):
#         polls = User.objects.all()
#         serializer = UserSerializer(polls, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(
#         request_body=PollSerializer,
#         operation_description="This endpoint for creating Poll Object"
#     )
#     def post(self, request):
#         serializer = PollSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class PollView(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         serializer = PollSerializer(poll)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         serializer = PollSerializer(data=request.data, instance=poll)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data={"message": "Object successfully updated"}, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         serializer = PollPatchSerializer(data=request.data, instance=poll)
#         if serializer.is_valid():
#             data = serializer.validated_data
#             for key, value in data.items():
#                 setattr(poll, key, value)
#             poll.save()
#             return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         poll.delete()
#         return Response(data={"message": "Object successfully deleted"}, status=status.HTTP_202_ACCEPTED)