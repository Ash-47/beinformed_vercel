from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass


class Categories(models.Model):
    category=models.CharField(max_length=20)
    followers=models.ManyToManyField(User,related_name="following",blank=True)

    def __str__(self):
        return f"{self.category}"
