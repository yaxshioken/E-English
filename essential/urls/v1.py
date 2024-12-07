from os.path import basename
from tkinter.font import names

from django.urls import path
from rest_framework import routers

from account import views
from essential.serializers import CheckWordSerializer
from essential.views import BookCreateViewSet, UnitViewSet, VocabularyViewSet, CheckView, ChekWordAPIView

router=routers.DefaultRouter()

router.register('book',BookCreateViewSet,basename='book')
router.register('units',UnitViewSet,basename='unit')
router.register('vocabularies',VocabularyViewSet,basename='vocabularies')

urlpatterns = router.urls
urlpatterns += [path('check/',CheckView.as_view(),name='check'),]
urlpatterns += [path('checkword/',ChekWordAPIView.as_view(),name='check'),]