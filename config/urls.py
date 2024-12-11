
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView

from config.swaggers import swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls.v1")),
    path("books/", include("essential.urls.v1")),
]
urlpatterns += swagger_urlpatterns