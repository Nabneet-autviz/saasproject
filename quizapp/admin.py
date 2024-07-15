from django.contrib import admin
from .models import *
# Register your models here.
models_name=[Quiz,DifficultyRating,QuestionGroup,QuestionType,Question,QuestionChoice,Picture,Answers]
admin.site.register(models_name)
