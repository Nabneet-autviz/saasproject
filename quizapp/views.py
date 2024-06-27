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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)

class DifficultyRatingViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = DifficultyRating.objects.all()
    serializer_class = DifficultyRatingSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)


class QuestionGroupViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionGroup.objects.all()
    serializer_class = QuestionGroupSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)


class QuestionTypeViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)


class QuestionViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)


class AnswersViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = Answers.objects.all()
    serializer_class = AnswersSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)


class QuestionChoiceViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionChoice.objects.all()
    serializer_class = QuestionChoiceSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)
