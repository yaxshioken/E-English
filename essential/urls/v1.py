from django.urls import path

from essential.views import (BookView, CheckView, CheckWordAPIView, UnitView,
                             VocabularyView)

urlpatterns = [
    path("book/", BookView.as_view(), name="book"),
    path("book/<int:id>/", BookView.as_view(), name="book"),
    path("unit/", UnitView.as_view(), name="unit"),
    path("unit/<int:id>/", UnitView.as_view(), name="unit"),
    path("vocabularies/", VocabularyView.as_view(), name="vocabulary"),
    path("vocabularies/<int:id>/", VocabularyView.as_view(), name="vocabulary"),
    path("check/", CheckView.as_view(), name="check"),
    path("checkword/", CheckWordAPIView.as_view(), name="checkword"),
]
