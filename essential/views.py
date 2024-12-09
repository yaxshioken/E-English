from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from essential.models import Book, Unit, Vocab

from essential.serializers import (BookSerializer,
                                   CheckinYourselfSerializer,
                                   CheckWordSerializer,
                                   UnitSerializer,
                                   VocabSerializer)


class BookView(APIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'level']
    search_fields = ['name', 'level']
    my_tags = ("book",)

    def get(self, request, id=None):
        """
        this is queryset objects all given by id, name, level
        """
        if id:
            book = get_object_or_404(Book, pk=id)
            serializer = self.serializer_class(book)
            return Response(serializer.data)

        queryset = Book.objects.all()
        name = self.request.query_params.get('name', None)
        level = self.request.query_params.get('level', None)

        if name:
            queryset = queryset.filter(name__icontains=name)

        if level:
            try:
                queryset = queryset.filter(level=level)
            except ValueError:
                return Response({"detail": "level butun son bo'lishi kerak"},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        book = get_object_or_404(Book, id=id)
        serializer = self.serializer_class(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        book = get_object_or_404(Book, id=id)
        serializer = self.serializer_class(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id=None):
        book = get_object_or_404(Book, id=id)
        try:
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message': f"ERROR:{e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Successfully deleted!!!"}, status=status.HTTP_204_NO_CONTENT)


class UnitView(APIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'unit_num', 'book']
    search_fields = ['name', 'unit_num', 'book']
    my_tags = ("unit",)

    def get(self, request, id=None):
        """
        this is queryset objects all given by id, name, unit_num, book
        """
        if id:
            unit = get_object_or_404(Unit, pk=id)
            serializer = self.serializer_class(unit)
            return Response(serializer.data)

        queryset = Unit.objects.all()
        name = self.request.query_params.get('name',None)
        unit_num = self.request.query_params.get('unit_num',None)
        book = self.request.query_params.get('book',None)
        if name:
            queryset = queryset.filter(name__icontains=name)

        if unit_num:
            try:
                queryset = queryset.filter(unit_num__in=unit_num)
            except ValueError:
                return Response({"detail": "unit_num butun son bo'lishi kerak"},
                                status=status.HTTP_400_BAD_REQUEST)
        if book:
            try:
                queryset = queryset.filter(book=book)
            except ValueError:
                return Response({"detail": "book_id butun son bo'lishi kerak"}, )

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        unit = get_object_or_404(Unit, id=id)
        serializer = self.serializer_class(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        unit = get_object_or_404(Unit, id=id)
        serializer = self.serializer_class(unit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        unit = get_object_or_404(Unit, id=id)
        try:
            unit.delete()

            return Response(data="Successfully deleted!!!", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VocabularyView(APIView):
    serializer_class = VocabSerializer
    queryset = Vocab.objects.all()
    my_tags = ("vocabulary",)
    def get(self, request, id=None):
        """ This is queryset objects all given by id, en, uz, unit. """
        if id:
            vocab = get_object_or_404(Vocab, pk=id)
            serializer = self.serializer_class(vocab)
            return Response(serializer.data)
        queryset = Vocab.objects.all()
        en = request.query_params.get('en', None)
        uz = request.query_params.get('uz', None)
        unit = request.query_params.get('unit', None)
        if en:
            queryset = queryset.filter(en__icontains=en)
        if uz: queryset = queryset.filter(uz__icontains=uz)
        if unit: queryset = queryset.filter(unit=unit)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        vocab = get_object_or_404(Vocab, id=id)
        serializer = self.serializer_class(vocab, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id=None):
        vocab = get_object_or_404(Vocab, id=id)
        serializer = self.serializer_class(vocab, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        vocab = get_object_or_404(Vocab, id=id)
        try:
            vocab.delete()
            return Response({"message": "Successfully deleted!!!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckView(APIView):
    queryset = Vocab.objects.all()
    serializer_class = CheckinYourselfSerializer
    my_tags = ("check",)

    def post(self, request, *args, **kwargs):
        book = request.data["book"]
        unit = request.data["unit"]
        unit = Unit.objects.filter(book=book, unit_num=unit).first()

        if not unit:
            return Response(
                {"error": "Unit not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        vocab = Vocab.objects.filter(unit=unit)
        serializer = VocabSerializer(vocab, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckWordAPIView(APIView):
    my_tags = ("checkword",)
    serializer_class = CheckWordSerializer

    def post(self, request):
        word = request.data["word"]
        soz = Vocab.objects.filter(en=word)
        if soz.exists():
            serializer = VocabSerializer(soz, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Vocab not found"}, status=status.HTTP_400_BAD_REQUEST
            )
