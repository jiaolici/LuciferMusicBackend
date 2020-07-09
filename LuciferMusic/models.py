from django.db import models

# Create your models here.
# django 2.2.3
# restframework 3.10.1
# jwt 1.11.0
# python 3.7.4
# django-cors-headers
from django.contrib.auth.models import AbstractUser
from django.db import models

# 扩展User类
class UserProfile(AbstractUser):
    avatar = models.ImageField()
    introduction = models.CharField(max_length=100)
    gender = models.CharField(max_length=2,choices=(("男","男"),("女","女")))
    birthday = models.DateField(default="2019-1-1")
    city = models.CharField(max_length=10)
    class Meta(AbstractUser.Meta):
        pass