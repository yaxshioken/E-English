
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from config.swaggers import swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls.v1")),
    path("books/", include("essential.urls.v1")),
    path("units/", include("essential.urls.v2")),
    path("vocabs/", include("essential.urls.v3")),
]
urlpatterns += swagger_urlpatterns
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]