from django.urls import path

from account.views import (CheckCodeView, CustomTokenObtainPairView,
                           CustomTokenRefreshView, LoginView, RegisterView,
                           SendEmailCodeView)

urlpatterns = [
    path("sendcode/", SendEmailCodeView.as_view(), name="send-email-code"),
    path("verify/", CheckCodeView.as_view(), name="checkcode"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", CustomTokenRefreshView  .as_view(), name="token_refresh"),
]
