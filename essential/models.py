from os.path import join

from django.db.models import Model, CharField, PositiveIntegerField, ImageField, ForeignKey, CASCADE, FileField

from config.settings import BASE_DIR


class Book(Model):
    name = CharField(max_length=255)
    level = PositiveIntegerField(default=1)
    image = ImageField(upload_to='media/books/')

class Unit(Model):
    name = CharField(max_length=255)
    unit_num = PositiveIntegerField(default=1)
    book = ForeignKey('Book' , CASCADE , related_name='units')

class Vocab(Model):
    uz = CharField(max_length=255)
    en = CharField(max_length=255)
    audio = FileField(upload_to='media/vocab/audio/')
    unit = ForeignKey('Unit' , CASCADE , related_name='vocabs')