from django.urls import path

from essential.views import (BookView, CheckView, CheckWordAPIView, UnitView,
                             VocabularyView, BookRetrieveUpdateDeleteAPIView, UnitRetrieveUpdateDeleteAPIView,
                             VocabularyRetrieveUpdateDeleteAPIView)

urlpatterns = [
    path("book/", BookView.as_view(), name="book"),
    path("book/<int:id>/", BookRetrieveUpdateDeleteAPIView.as_view(), name="book"),


]
