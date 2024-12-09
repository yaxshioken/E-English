from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = slugify(self.email)
        super(User, self).save(*args, **kwargs)
        self.save()
        return self
