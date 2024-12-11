from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import (CASCADE, CharField, FileField, ForeignKey,
                              ImageField, Model, PositiveIntegerField)


class Book(Model):
    name = CharField(max_length=255, unique=True)
    level = PositiveIntegerField()
    image = ImageField(upload_to="media/books/")
    unique_together = (("name", "level"),)

class Unit(Model):
    name = CharField(max_length=255, unique=True)
    unit_num = PositiveIntegerField( validators=[MinValueValidator(1), MaxValueValidator(6)])
    book = ForeignKey("Book", CASCADE, related_name="units")
    unique_together = (("book", "unit_num"),)


class Vocab(Model):
    uz = CharField(max_length=255)
    en = CharField(max_length=255,unique=True)
    audio = FileField(upload_to="media/vocab/audio/")
    unit = ForeignKey("Unit", CASCADE, related_name="vocabs")
