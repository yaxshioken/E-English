from rest_framework import serializers

from essential.models import Book, Unit, Vocab
from essential.utils import generate_audio_world


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','name','level','image')
        read_only_fields = ('id',)


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id','name','unit_num','book')
        read_only_fields = ('id',)

class VocabSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vocab
        fields=('id','uz','en','audio','unit')
        read_only_fields=('id','audio')

    def validate(self, attrs):
        en = attrs.get("en")
        path = generate_audio_world(en)
        attrs["audio"] = path
        return attrs


class CheckinYourselfSerializer(serializers.Serializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())


class CheckWordSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=50)
class UnitFilterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        exclude = 'book',

class VocabFilterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocab
        exclude = 'audio',"unit"
