from django.urls import path

from essential.views import (CheckView, CheckWordAPIView, VocabularyRetrieveUpdateDeleteAPIView, VocabularyView)

urlpatterns = [
    path("vocabularies/", VocabularyView.as_view(), name="vocabulary"),
    path("vocabularies/<int:id>/", VocabularyRetrieveUpdateDeleteAPIView.as_view(), name="vocabulary"),
    path("check/", CheckView.as_view(), name="check"),
    path("checkword/", CheckWordAPIView.as_view(), name="checkword")]
