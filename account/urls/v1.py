
from django.urls import path

from account.views import (CheckCodeView, LoginView, RegisterView,
                           SendEmailCodeView, CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView)

urlpatterns = ([
    path("sendcode/", SendEmailCodeView.as_view(), name="send-email-code"),
    path("verify/", CheckCodeView.as_view(), name="checkcode"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    ])
