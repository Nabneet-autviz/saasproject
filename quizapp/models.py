from django.db import models
from authentication.models import *

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class DifficultyRating(BaseModel):
    difficultyrating = models.CharField(max_length=100)

    def __str__(self):
        return self.difficultyrating
class Quiz(BaseModel):
    quiz_name = models.CharField(max_length=500,default=False)
    quiz_description  = models.TextField()
    difficultyrating = models.ForeignKey(DifficultyRating, on_delete=models.CASCADE,related_name="difficulity_quiz")
    def __str__(self):
         return self.quiz_name


class QuestionGroup(BaseModel):
    questiongroup = models.CharField(max_length=100)

    def __str__(self):
        return self.questiongroup


class QuestionType(BaseModel):
    questiontype = models.CharField(max_length=100)

    def __str__(self):
        return self.questiontype
    

class Question(BaseModel):
    
    quizz = models.ForeignKey(Quiz, on_delete=models.CASCADE,related_name="quizz_name")
    content = models.CharField(max_length=255)
    difficultyrating = models.ForeignKey(DifficultyRating, on_delete=models.CASCADE,related_name="difficulity_question")
    questiongroup = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE,related_name="group_question")
    questiontype = models.ForeignKey(QuestionType, on_delete=models.CASCADE,related_name="type_question")
    answer = models.CharField(max_length=500)
    
    

    def __str__(self):
        return self.content
    
class Picture(BaseModel):
    picture = models.FileField(upload_to='media/', blank=True, null=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name="picture_question")
    def __str__(self):
        return self.question
    

class Answers(BaseModel):
    answer = models.CharField(max_length=5509)
    student= models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_customer")
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name="user_question")
    def __str__(self):
        return self.answer
    

class QuestionChoice(BaseModel):

    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name="question")
    question_choice = models.CharField(max_length=255)
    def __str__(self):
        return self.question_choice
    