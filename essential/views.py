from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import serialize

from essential.models import Book, Unit, Vocab
from essential.serializers import (BookSerializer, CheckinYourselfSerializer,
                                   CheckWordSerializer, UnitSerializer,
                                   VocabSerializer)


class BookView(APIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    my_tags = ("book",)
    @action(detail=True, methods=["POST"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(methods=['GET'], detail=True)
    def get(self, request,id=None):
        if id:
            book=get_object_or_404(Book, pk=id)
            serializer =self.serializer_class(book)
            return Response(serializer.data)
        else:
            books = Book.objects.all()
            serializer = self.serializer_class(books, many=True)
            return Response(serializer.data)
    @action(methods=['PUT'], detail=True)
    def put(self, request, id=None):
        book = get_object_or_404(Book, id=id)
        serializer = self.serializer_class(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(methods='PATCH', detail=True)
    def patch(self, request, id=None):
        book = get_object_or_404(Book, id=id)
        serializer = self.serializer_class(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    @action(methods='DELETE', detail=True)
    def delete(self, request, id=None):
        book = get_object_or_404(Book, id=id)
        try:
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message':f"ERROR:{e}"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Successfully deleted!!!"},status=status.HTTP_204_NO_CONTENT)

class UnitView(APIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    my_tags = ("unit",)
    @action(methods=['GET'], detail=True,)
    def get(self, request,id=None):
        if id:
            unit=get_object_or_404(Unit, id=id)
            serializer = self.serializer_class(unit)
            return Response(serializer.data)
        else:
            unit=Unit.objects.all()
            serializer = self.serializer_class(unit, many=True)
            return Response(serializer.data)
    @action(methods=['POST'], detail=True)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=True)
    def put(self, request, id=None):
        unit = get_object_or_404(Unit, id=id)
        serializer = self.serializer_class(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(methods=['PATCH'], detail=True)
    def patch(self, request, id=None):
        unit = get_object_or_404(Unit, id=id)
        serializer = self.serializer_class(unit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(methods='DELETE', detail=True)
    def delete(self,request, id=None):
        unit = get_object_or_404(Unit, id=id)
        try:
            unit.delete()

            return Response(data="Successfully deleted!!!",status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)

class VocabularyView(APIView):
    queryset = Vocab.objects.all()
    serializer_class = VocabSerializer
    my_tags = ("vocab",)

    @action(methods=['POST'], detail=True)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True)
    def get(self, request,id=None):
        if id:
            vocab=get_object_or_404(Vocab, id=id)
            serializer = self.serializer_class(vocab)
            return Response(serializer.data)
        else:
            vocabs = Vocab.objects.all()
            serializer = self.serializer_class(vocabs, many=True)
            return Response(serializer.data)

    @action(methods=['PUT'], detail=True)
    def put(self, request, id=None):
        vocab = get_object_or_404(Vocab, id=id)
        serializer = self.serializer_class(vocab, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['PATCH'], detail=True)
    def patch(self, request, id=None):
        vocab= get_object_or_404(Vocab, id=id)
        serializer=self.serializer_class(vocab,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['DELETE'], detail=True)
    def delete(self, request, id=None):
        vocab = get_object_or_404(Vocab, id=id)
        try:
            vocab.delete()
            return Response({"message":"Successfully deleted!!!"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)


class CheckView(APIView):
    queryset = Vocab.objects.all()
    serializer_class = CheckinYourselfSerializer
    my_tags = ("check",)

    @action(methods=['POST'], detail=True)
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
        # unit=Unit.objects.filter(book=book, unit_num=unit)
        # vocab=Vocab.objects.filter(unit=unit)[0:]
        # return Response(VocabSerializer(data=vocab,many=True), status=status.HTTP_200_OK)


class CheckWordAPIView(APIView):
    my_tags = ("checkword",)
    serializer_class = CheckWordSerializer
    @action(methods=['POST'],detail=True)
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
