from django.urls import path

from essential.views import (BookView, CheckView, CheckWordAPIView, UnitView,
                             VocabularyView, BookRetrieveUpdateDeleteAPIView, UnitRetrieveUpdateDeleteAPIView,
                             VocabularyRetrieveUpdateDeleteAPIView)

urlpatterns = [
    path("book/", BookView.as_view(), name="book"),
    path("book/<int:id>/", BookRetrieveUpdateDeleteAPIView.as_view(), name="book"),
    path("unit/", UnitView.as_view(), name="unit"),
    path("unit/<int:id>/", UnitRetrieveUpdateDeleteAPIView.as_view(), name="unit"),
    path("vocabularies/", VocabularyView.as_view(), name="vocabulary"),
    path("vocabularies/<int:id>/", VocabularyRetrieveUpdateDeleteAPIView.as_view(), name="vocabulary"),
    path("check/", CheckView.as_view(), name="check"),
    path("checkword/", CheckWordAPIView.as_view(), name="checkword"),
]
