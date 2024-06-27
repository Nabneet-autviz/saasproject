from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class QuizViewset(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes= [IsAuthenticated]

class DifficultyRatingViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = DifficultyRating.objects.all()
    serializer_class = DifficultyRatingSerializer

class QuestionGroupViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionGroup.objects.all()
    serializer_class = QuestionGroupSerializer

class QuestionTypeViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer

class QuestionViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswersViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer

class QuestionChoiceViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer