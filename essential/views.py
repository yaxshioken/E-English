import json
import random
from http import HTTPStatus
from random import shuffle

from attr import dataclass
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from pandas.core.dtypes.inference import is_float
from redis import Redis
from rest_framework import status
from rest_framework.exceptions import ValidationError

from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Result
from essential.models import Book, Unit, Vocab

from essential.serializers import (BookSerializer,
                                   CheckinYourselfSerializer,
                                   CheckWordSerializer,
                                   UnitSerializer,
                                   VocabSerializer)


class BookView(APIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['name', 'level']
    my_tags = ("book",)

    def get(self, request):
        """
          Barcha kitoblar ro'yxatini olish
          Ro'yxatni kitob nomi yoki darajasi bo'yicha filtrlash mumkin (katta-kichik harflarga sezgir emas).

          So'rov Parametrlari:
            - name: Kitob nomi bo'yicha filtr .
            - level: Kitob darajasi bo'yicha filtr.
        """

        queryset = Book.objects.all()
        name = self.request.query_params.get('name', None)
        level = self.request.query_params.get('level', None)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) or Q(level__in=search))
        if name:
            queryset = queryset.filter(name__contains=name)

        if level:
            try:
                queryset = queryset.filter(level=level)
            except ValueError:
                return Response({"detail": "level butun son bo'lishi kerak"},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Yangi kitob yaratish uchun kitob ma'lumotlarini yuboring.Rasm keyinchalik yuklanadi",
        request_body=BookSerializer,
    )
    def post(self, request):
        """

            Tavsif: Yangi kitob yaratish uchun zarur bo'lgan ma'lumotlarni yuboring.
            So'rov Tanasi:
            name: Kitob nomi.
            level: Kitob darajasi (masalan: boshlang'ich, o'rtacha, ilg'or).
        Javoblar:
            201 Created: Kitob muvaffaqiyatli yaratildi.
            400 Bad Request: Noto'g'ri ma'lumot yuborilgan bo'lsa, xato javobi.


        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookRetrieveUpdateDeleteAPIView(APIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    my_tags = ("book",)

    def get(self, request, id):
        """
           Tavsif: Bitta kitobni ID raqami bo'yicha olish.
           So'rov Parametrlari:
                id: Kitobning ID raqami.
           Javoblar:
                200 OK: Kitob muvaffaqiyatli topildi.
                404 Not Found: Kitob topilmadi.
        """
        book = get_object_or_404(Book, pk=id)
        serializer = self.serializer_class(book)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Mavjud kitobni IDsi bo'yicha yangilash barcha ma'lumotlarini yuboring.",
        request_body=BookSerializer,
    )
    def put(self, request, id):
        """
        Tavsif: Mavjud kitobni ID bo'yicha yangilash.
        So'rov Tanasi:
            name: Yangi kitob nomi.
            level: Yangi kitob darajasi.
        Javoblar:
            200 OK: Kitob muvaffaqiyatli yangilandi.
            400 Bad Request: Noto'g'ri ma'lumot yuborilgan bo'lsa, xato javobi.
            404 Not Found: Kitob topilmadi.
        """
        book = get_object_or_404(Book, id=id)
        serializer = self.serializer_class(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description=" Mavjud kitobni qisman yangilash uchun zarur bo‘lgan url",
        request_body=BookSerializer,
    )
    def patch(self, request, id):
        """
        Tavsif: Mavjud kitobni qisman yangilash.
        So'rov Tanasi:
            name (ixtiyoriy): Yangi kitob nomi.
            level (ixtiyoriy): Yangi kitob darajasi.
        Javoblar:
            200 OK: Faoliyat muvaffaqiyatli amalga oshirildi va o'zgartirilgan maydonlar qaytariladi.
            404 Not Found: Kitob topilmadi.
            400 Bad Request: Noto'g'ri ma'lumot yuborilgan bo'lsa, xato javobi.
        """
        book = get_object_or_404(Book, id=id)
        serializer = self.serializer_class(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Mavjud kitobni ID-si bo'yicha o'chirish",
    )
    def delete(self, request, id):
        """
        Tavsif: Kitobni ID raqami bo'yicha o'chirish.
        So'rov Parametrlari:
            id: Kitobning ID raqami.
        Javoblar:
            200 OK: Kitob muvaffaqiyatli o'chirildi.
            404 Not Found: Kitob topilmadi.
        """
        book = get_object_or_404(Book, id=id)
        book.delete()
        return Response(data={"message": "Kitob muvaffaqiyatli o'chirildi."}, status=status.HTTP_200_OK)


class UnitView(APIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    filter_backends = (SearchFilter,)
    filterset_fields = ('name','unit_num','book')
    search_fields = ['name', 'unit_num', 'book']
    my_tags = ("unit",)

    def get(self, request):
        """
       Tavsif: Unitlar ro'yxatini olish. nomi, unit raqami yoki kitob bo'yicha filtrlanishi mumkin.
        So'rov Parametrlari:
            name: Unit nomi bo'yicha filtr
            unit_num: Unit raqami bo'yicha filtr.
            book: Kitob IDsi bo'yicha filtr.
        Javoblar:
            200 OK: Unitlar ro'yxati muvaffaqiyatli qaytarildi.
            400 Bad Request: Noto'g'ri ma'lumot yuborilgan bo'lsa, xato javobi.
        """

        queryset = Unit.objects.all()
        name = self.request.query_params.get('name', None)
        unit_num = self.request.query_params.get('unit_num', None)
        book = self.request.query_params.get('book', None)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) or Q(unit_num__in=search) | Q(book_id__in=search))
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

    @swagger_auto_schema(
        operation_description="Yangi Unit yaratish",
        request_body=UnitSerializer,
    )
    def post(self, request):
        """
        Tavsif: Yangi unitni yaratish.
        So'rov Tanasi:
            name: Unit nomi.
            unit_num: Unit raqami.
            book: Kitob IDsi.
        Javoblar:
            201 Created: Unit muvaffaqiyatli yaratildi.
            400 Bad Request: Noto'g'ri ma'lumot yuborilgan bo'lsa, xato javobi
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnitRetrieveUpdateDeleteAPIView(APIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    my_tags = ("unit",)

    def get(self, request, id):
        """
        Tavsif: Unitni ID bo'yicha olish.
        So'rov Parametrlari:
            id: Unitning ID raqami.
        Javoblar:
            200 OK: Unit muvaffaqiyatli topildi.
            404 Not Found: Unit topilmadi.
        """
        unit = get_object_or_404(Unit, pk=id)
        serializer = self.serializer_class(unit)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Mavjud unitni yangilash.",
        request_body=UnitSerializer,
    )
    def put(self, request, id):
        """
            Tavsif: Mavjud unitni yangilash.
            So'rov Tanasi:
                name: Yangi unit nomi.
                unit_num: Yangi unit raqami.
                book_id: Kitob IDsi.
            Javoblar:
                200 OK: Unit muvaffaqiyatli yangilandi.
                400 Bad Request: Noto'g'ri ma'lumot yuborilgan bo'lsa, xato javobi.
                404 Not Found: Unit topilmadi.
        """
        unit = get_object_or_404(Unit, id=id)
        serializer = self.serializer_class(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Mavjud unitni qisman yangilash.",
        request_body=UnitSerializer,
    )
    def patch(self, request, id):
        """
        Tavsif: Unitni qisman yangilash.
        So'rov Tanasi:
            name (ixtiyoriy): Yangi unit nomi.
            unit_num (ixtiyoriy): Unit raqami.
            book (ixtiyoriy): Kitob IDsi.
        Javoblar:
            200 OK: Unit muvaffaqiyatli yangilandi.
            400 Bad Request: Noto'g'ri ma'lumot yuborilgan bo'lsa, xato javobi.
            404 Not Found: Unit topilmadi.
        """
        unit = get_object_or_404(Unit, id=id)
        serializer = self.serializer_class(unit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Mavjud unitni ID-isi bo'yicha o'chirish"
    )
    def delete(self, request, id):
        """
        Tavsif: Unitni ID raqami bo'yicha o'chirish.
        So'rov Parametrlari:
            id: Unitning ID raqami.
        Javoblar:
            204 No Content: Unit  muvaffaqiyatli o'chirildi.
            404 Not Found: Unit topilmadi.
        """
        unit = get_object_or_404(Unit, id=id)
        try:
            if unit.delete():
                    return Response({"message":"Unit  muvaffaqiyatli o'chirildi."},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=f"Xato:{str(e)}",status=status.HTTP_404_NOT_FOUND)

class VocabularyView(APIView):
    serializer_class = VocabSerializer
    queryset = Vocab.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('en', 'uz', 'unit')
    my_tags = ("vocabulary",)

    def get(self, request):
        """
            Tavsif: Barcha so'zlarni olish. Bu en, uz yoki unit  ustunlari bo'yicha filtrlanishi mumkin.
            So'rov Parametrlari:
                en: Inglizcha so'z .
                uz: O'zbekcha tarjima .
                unit: Unit IDsi.
            Javoblar:
                200 OK: So'z muvaffaqiyatli qaytarildi.
                400 Bad Request: Noto'g'ri ma'lumot yuborilgan bo'lsa, xato javobi.
        """

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

    @swagger_auto_schema(operation_description=""" Yangi so'zlarni yaratish.""",
                         request_body=VocabSerializer)
    def post(self, request):
        """
        Tavsif: Yangi so'z yaratish.
        So'rov Tanasi:
            en: Inglizcha so'z.
            uz: O'zbekcha tarjima.
            unit: Unit IDsi.
        Javoblar:
            201 Created:So'z muvaffaqiyatli yaratildi.
            400 Bad Request: Noto'g'ri ma'lumot yuborilgan bo'lsa, xato javobi.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VocabularyRetrieveUpdateDeleteAPIView(APIView):
    serializer_class = VocabSerializer
    queryset = Vocab.objects.all()
    my_tags = ("vocabulary",)

    def get(self, request, id):
        """
        So'zlarni ID-isi bo'yicha olish.
         """
        vocab = get_object_or_404(Vocab, pk=id)
        serializer = self.serializer_class(vocab)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="""Mavjud so'zlarni yangilash""",
                         request_body=VocabSerializer)
    def put(self, request, id):

        """
        Tavsif:So'zlarni yangilash.
        So'rov Tanasi:
            en: Yangi inglizcha so'z.
            uz: Yangi o'zbekcha tarjima.
            unit: Yangi unit IDsi.
        Javoblar:
            200 OK:So'zlar muvaffaqiyatli yangilandi.
            404 Not Found: So'z topilmadi.
        """
        vocab = get_object_or_404(Vocab, id=id)
        serializer = self.serializer_class(vocab, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="""Mavjud so'zlarni qisman yangilash.""",
                         request_body=VocabSerializer, )
    def patch(self, request, id):
        """
        Tavsif: So'zlarni qisman yangilash.
        So'rov Tanasi:
            en (ixtiyoriy): Yangi inglizcha so'z.
            uz (ixtiyoriy): Yangi o'zbekcha tarjima.
            unit (ixtiyoriy): Yangi unit IDsi.
        Javoblar:
            200 OK: So'z muvaffaqiyatli yangilandi.
            400 Bad Request: Noto'g'ri ma'lumot yuborilgan bo'lsa, xato javobi.
        """
        vocab = get_object_or_404(Vocab, id=id)
        serializer = self.serializer_class(vocab, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="So'zni o'chirish",
    )
    def delete(self, request, id):
        """
        Tavsif: So'zni o'chirish.
        So'rov Parametrlari:
            id: So'z IDsi.
        Javoblar:
            204 No Content: So'z muvaffaqiyatli o'chirildi.
            404 Not Found: So'z topilmadi.
        """
        vocab = get_object_or_404(Vocab, id=id)
        try:
            vocab.delete()
            return Response({"message": "So'z muvaffaqiyatli o'chirildi."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)






class CheckView(APIView):
    queryset = Vocab.objects.all()
    serializer_class = CheckinYourselfSerializer
    my_tags = ("checkword",)

    @swagger_auto_schema(
        operation_description="Kitob va unit bo'yicha So'zlarni tekshirish.",
        request_body=CheckinYourselfSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        Tavsif: Kitob va unit bo'yicha So'zlarni tekshirish.
        So'rov Tanasi:
            book: Kitob IDsi.
            unit: Unit raqami.
        Javoblar:
            200 OK: Tekshirilgan So'zlar ro'yxati qaytariladi.
        """
        book = request.data["book_id"]
        unit_num = request.data["unit_id"]
        try:
            unit = Unit.objects.filter(Q(book=book) & Q(unit_num=unit_num)).first()
        except Unit.DoesNotExist:
            raise ValidationError("No unit found for the provided book and unit numbers.")

        vocabs = list(Vocab.objects.filter(unit=unit).values_list('id', flat=True))
        if not vocabs:
            raise ValidationError('No vocabs found')

        redis = Redis(decode_responses=True)
        random_vocab = random.choice(vocabs)
        vocabs.remove(random_vocab)
        data = {"correct": 0, "incorrect": 0, "unit_id": unit.id, "vocabs_id": vocabs, "finish": False}
        redis.set(request.user.id, json.dumps(data))

        vocab = Vocab.objects.filter(id=random_vocab).first()
        vocab_data = VocabSerializer(vocab).data
        return Response({"data": vocab_data}, status=status.HTTP_200_OK)


class CheckWordAPIView(APIView):
    my_tags = ("checkword",)
    serializer_class = CheckWordSerializer

    @swagger_auto_schema(
        operation_description="Inglizcha so'z bo'yicha So'zlarni tekshirish.",
        request_body=CheckWordSerializer,

    )
    def post(self, request):
        """
        Tavsif: Inglizcha so'z bo'yicha So'zlarni tekshirish.
        So'rov Tanasi:
            word: Inglizcha so'z.
        Javoblar:
            200 OK: So'z mavjud bo'lsa, So'zlar qaytariladi.
            400 Bad Request: So'z topilmasa, xato javobi qaytariladi.
        """
        vocab_id = request.data["vocab_id"]
        word = request.data["word"]
        soz = Vocab.objects.filter(id=vocab_id).first()
        redis = Redis(decode_responses=True)
        r_data = json.loads(redis.get(request.user.id))
        if  not r_data:
            return Response(r_data, HTTPStatus.OK)
        is_correct = soz.en.lower() == word.lower()
        r_data['correct'] += is_correct
        r_data['incorrect'] += not is_correct
        if not r_data['vocabs_id']:
            r_data['finish'] = True
            redis.delete(request.user.id)
            r_data['last_question'] = is_correct
            return Response(r_data, HTTPStatus.OK)

        vocabs_id = list(r_data['vocabs_id'])
        random_vocab = random.choice(vocabs_id)
        vocabs_id.remove(random_vocab)

        r_data['last_question'] = is_correct
        r_data['vocabs_id'] = vocabs_id
        redis.set(request.user.id, json.dumps(r_data))
        vocab = Vocab.objects.filter(id=random_vocab).first()
        vocab_data = VocabSerializer(instance=vocab).data
        return Response(data=vocab_data, status=status.HTTP_200_OK)


class CheckView(APIView):
    queryset = Vocab.objects.all()
    serializer_class = CheckinYourselfSerializer
    my_tags = ("checkword",)

    @swagger_auto_schema(
        operation_description="Kitob va unit bo'yicha So'zlarni tekshirish.",
        request_body=CheckinYourselfSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        Tavsif: Kitob va unit bo'yicha So'zlarni tekshirish.
        So'rov Tanasi:
            book: Kitob IDsi.
            unit: Unit raqami.
        Javoblar:
            200 OK: Tekshirilgan So'zlar ro'yxati qaytariladi.
        """
        book = request.data["book_id"]
        unit_num = request.data["unit_id"]
        try:
            unit = Unit.objects.filter(Q(book=book) & Q(unit_num=unit_num)).first()
        except Unit.DoesNotExist:
            raise ValidationError("No unit found for the provided book and unit numbers.")

        vocabs = list(Vocab.objects.filter(unit=unit).values_list('id', flat=True))
        if not vocabs:
            raise ValidationError('No vocabs found')

        redis = Redis(decode_responses=True)
        random_vocab = random.choice(vocabs)
        vocabs.remove(random_vocab)
        data = {"correct": 0, "incorrect": 0, "unit_id": unit.id, "vocabs_id": vocabs, "finish": False}
        redis.set(request.user.id, json.dumps(data))

        vocab = Vocab.objects.filter(id=random_vocab).first()
        vocab_data = VocabSerializer(vocab).data
        return Response({"data": vocab_data}, status=status.HTTP_200_OK)


class CheckWordAPIView(APIView):
    my_tags = ("checkword",)
    serializer_class = CheckWordSerializer

    @swagger_auto_schema(
        operation_description="Inglizcha so'z bo'yicha So'zlarni tekshirish.",
        request_body=CheckWordSerializer,

    )
    def post(self, request):
        """
        Tavsif: Inglizcha so'z bo'yicha So'zlarni tekshirish.
        So'rov Tanasi:
            word: Inglizcha so'z.
        Javoblar:
            200 OK: So'z mavjud bo'lsa, So'zlar qaytariladi.
            400 Bad Request: So'z topilmasa, xato javobi qaytariladi.
        """
        vocab_id = request.data["vocab_id"]
        word = request.data["word"]
        soz = Vocab.objects.filter(id=vocab_id).first()
        redis = Redis(decode_responses=True)
        r_data = json.loads(redis.get(request.user.id))
        if  not r_data:
            return Response(r_data, HTTPStatus.OK)
        is_correct = soz.en.lower() == word.lower()
        r_data['correct'] += is_correct
        r_data['incorrect'] += not is_correct
        if not r_data['vocabs_id']:
            r_data['finish'] = True
            redis.delete(request.user.id)
            r_data['last_question'] = is_correct
            return Response(r_data, HTTPStatus.OK)

        vocabs_id = list(r_data['vocabs_id'])
        random_vocab = random.choice(vocabs_id)
        vocabs_id.remove(random_vocab)

        r_data['last_question'] = is_correct
        r_data['vocabs_id'] = vocabs_id
        redis.set(request.user.id, json.dumps(r_data))
        vocab = Vocab.objects.filter(id=random_vocab).first()
        vocab_data = VocabSerializer(instance=vocab).data
        return Response(data=vocab_data, status=status.HTTP_200_OK)
