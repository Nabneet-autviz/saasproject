from django.db import models
from django.contrib.auth.models import AbstractUser

class Roles(models.IntegerChoices):
    ADMIN = 0, 
    STUDENT = 1, 



class ClassName(models.Model):
    class_name = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_name
class CustomUser(AbstractUser):

    
    email = models.EmailField(unique=True)
    first_name = models.CharField( max_length=150, blank=True)
    last_name = models.CharField( max_length=150, blank=True)
    role = models.IntegerField(choices=Roles.choices,default=Roles.STUDENT)
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE,related_name="name_class")
    created_by_user = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ['email','first_name','last_name']

    def __str__(self):
        return self.username