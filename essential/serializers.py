from django.db.models import Q
from rest_framework import serializers

from essential.models import Book, Unit, Vocab
from essential.utils import generate_audio_world


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id',]


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields=['id',]

class VocabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocab
        fields = '__all__'
        read_only_fields = ['id','audio']
    def validate(self, attrs):
        en = attrs.get('en')
        path = generate_audio_world(en)
        attrs['audio'] = path
        return attrs

class CheckinYourselfSerializer(serializers.Serializer):
    book_id=serializers.IntegerField()
    unit_id=serializers.IntegerField()

class CheckWordSerializer(serializers.Serializer):
    vocab_id=serializers.IntegerField()
    word=serializers.CharField(max_length=50)

class VocabTestSerializer(serializers.Serializer):
    # book_id=serializers.CharField(max_length=50)
    # unit_id=serializers.IntegerField()
    # unit=Unit.objects.filter(Q(book=book_id)&Q(unit=unit_id))
    pass

class VocabFilterModelSerializer:
    pass
class VocabTrySerializer:
    pass
class VocabCheckSerializer:
    pass

