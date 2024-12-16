from django.urls import path

from essential.views import (UnitView,UnitRetrieveUpdateDeleteAPIView)

urlpatterns = [
path("unit/", UnitView.as_view(), name="unit"),
path("unit/<int:id>/", UnitRetrieveUpdateDeleteAPIView.as_view(), name="unit"),]