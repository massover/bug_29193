from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass


class Dog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


