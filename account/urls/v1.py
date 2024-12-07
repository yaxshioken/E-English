from django.urls import path


from account.views import SendEmailCodeView, CheckCodeView, RegisterView, LoginView

urlpatterns = [
    path('sendcode/',SendEmailCodeView.as_view(),name='send-email-code'),
    path('verify/',CheckCodeView.as_view(),name='checkcode'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
]
