from django.db.migrations import serializer
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.views import RegisterView
from essential.models import Book, Unit, Vocab
from essential.serializers import BookCreateSerializer, UnitSerializer, VocabSerializer, CheckinYourselfSerializer, \
    CheckWordSerializer


class BookCreateViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer
    my_tags=('book',)
class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    my_tags=('unit',)
class VocabularyViewSet(viewsets.ModelViewSet):
    queryset = Vocab.objects.all()
    serializer_class = VocabSerializer
    my_tags=('vocab',)
class CheckView(CreateAPIView):
    queryset = Vocab.objects.all()
    serializer_class = CheckinYourselfSerializer
    my_tags=('check',)
    def post(self, request, *args, **kwargs):
        book=request.data['book']
        unit=request.data['unit']
        unit = Unit.objects.filter(book=book, unit_num=unit).first()

        if not unit:
            return Response({"error": "Unit not found"}, status=status.HTTP_400_BAD_REQUEST)

        vocab = Vocab.objects.filter(unit=unit)
        serializer = VocabSerializer(vocab, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # unit=Unit.objects.filter(book=book, unit_num=unit)
        # vocab=Vocab.objects.filter(unit=unit)[0:]
        # return Response(VocabSerializer(data=vocab,many=True), status=status.HTTP_200_OK)


class ChekWordAPIView(CreateAPIView):
    my_tags=('checkword',)
    serializer_class = CheckWordSerializer
    def post(self, request):
        word = request.data['word']
        soz=Vocab.objects.filter(en=word)
        if soz.exists():
            serializer = VocabSerializer(soz, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Vocab not found"}, status=status.HTTP_400_BAD_REQUEST)

