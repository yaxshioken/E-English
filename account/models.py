from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import CharField, TextField, CASCADE, ForeignKey, Model, SET_NULL, SmallIntegerField, \
    DateTimeField, ManyToManyField
from django.utils.text import slugify

from account.choices import OptionTest, ResultType
from essential.models import Unit


class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = ['password']
    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = slugify(self.email)
        super(User, self).save(*args, **kwargs)
        self.save()
        return self
class TestSection(models.Model):
    title = CharField(max_length=255)
    description = TextField()
    def __str__(self):
        return self.title
class Test(models.Model):
    question = TextField()
    a = CharField(max_length=255)
    b = CharField(max_length=255)
    c = CharField(max_length=255)
    d = CharField(max_length=255)
    right = CharField(max_length=255 , choices=OptionTest.choices)
    section_test = ForeignKey('TestSection' , CASCADE , related_name='tests')

class Result(Model):
    user_id = ForeignKey('User' , SET_NULL ,null=True , blank=True, related_name='results')
    correct = SmallIntegerField(default=0)
    incorrect = SmallIntegerField(default=0)
    quantity = SmallIntegerField()
    type = CharField(max_length=255 , choices=ResultType.choices)
    created_at = DateTimeField(auto_now_add=True)
    units = ManyToManyField(Unit , related_name='results')
    test_sections = ManyToManyField('TestSection' , related_name='results')