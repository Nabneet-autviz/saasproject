from django.db import models
from django.contrib.auth.models import AbstractUser

class Roles(models.IntegerChoices):
    admin = 0,
    student = 1       


class CustomUser(AbstractUser):
    
    role = models.IntegerField(choices=Roles,default=Roles.student)
    created_by_user = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.username