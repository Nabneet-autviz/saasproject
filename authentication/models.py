from django.db import models
from django.contrib.auth.models import AbstractUser

class Roles(models.IntegerChoices):
    ADMIN = 0, 
    STUDENT = 1, 

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField( max_length=150, blank=True)
    last_name = models.CharField( max_length=150, blank=True)
    role = models.IntegerField(choices=Roles.choices,default=Roles.STUDENT)
    created_by_user = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    REQUIRED_FIELDS = ['email','first_name','last_name']
    def __str__(self):
        return self.username