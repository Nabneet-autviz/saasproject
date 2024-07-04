from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
# from .pagination import *
from django_filters.rest_framework import DjangoFilterBackend
import json

# Create your views here.


class QuizViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = Quiz.objects.all().order_by('created_at')
    serializer_class = QuizSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["quiz_name","quiz_description","difficultyrating"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)

class DifficultyRatingViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = DifficultyRating.objects.all().order_by('created_at')
    serializer_class = DifficultyRatingSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["difficultyrating"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)


class QuestionGroupViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionGroup.objects.all().order_by('created_at')
    serializer_class = QuestionGroupSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["questiongroup"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)


class QuestionTypeViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionType.objects.all().order_by('created_at')
    serializer_class = QuestionTypeSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["questiontype"]


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)


class QuestionViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = Question.objects.all().order_by('created_at')
    serializer_class = QuestionSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["quizz","difficultyrating","questiongroup","questiontype"]

    def create(self, request, *args, **kwargs):
        print(request.data,"data")
        if request.data:

            response_data = []
            for index,question_data in enumerate(request.data['questions'][0]):

                question_dict = {
                    'content': question_data['content'],
                    'answer': question_data['answer'],
                    'difficultyrating': int(question_data['difficultyrating']),
                    'quizz': question_data['quizz'],
                    'questiontype': question_data['questiontype'],
                    'questiongroup': question_data['questiongroup'],
                    'picture': question_data['picture'] if  question_data['picture'] else None
                }
                
                # Create the Question instance
                serializer = self.get_serializer(data=question_dict)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                
                # Get the ID of the newly created question
                question_id = serializer.instance.id
                
                # Process options for this question
                options_data = []
                for option_data in question_data['options']:
                    option_dict = {
                        'question': question_id,
                        'question_choice': option_data['optionText']
                    }
                    options_data.append(option_dict)
                
                # Create options using OptionSerializer
                option_serializer = QuestionChoiceSerializer(data=options_data, many=True)
                option_serializer.is_valid(raise_exception=True)
                option_serializer.save()
                
                # Append serialized question data to response_data
                response_data.append(serializer.data)
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({"message":"Check your data"}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        data = request.data
        for question_data in request.data:
            picture = question_data.get('picture') if 'picture' in question_data else instance.picture

    
            if picture is None and not 'picture' in question_data:
                picture = None
            # if question_data['difficultyrating']:
            #     data=DifficultyRating.objects.filter(id=question_data['difficultyrating']).values_list('difficultyrating', flat=True).first()
            question_dict = {
                'content': question_data.get('content', instance.content),
                'answer': question_data.get('answer', instance.answer),
                'difficultyrating': int(question_data.get('difficultyrating', instance.difficultyrating.id)),
                'quizz': question_data.get('quizz', instance.quizz.id),
                'questiontype': question_data.get('questiontype', instance.questiontype.id),
                'questiongroup': question_data.get('questiongroup',  instance.questiongroup.id),
                'picture': picture
            }

            serializer = self.get_serializer(instance, data=question_dict, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            options_data = question_data.get('options', [])
            options_to_create = []
            for question_choice_data in options_data:
                question_choice_id = QuestionChoice.objects.get(id=question_choice_data['id'])
                if question_choice_id:
                    try:
                        question_choice_instance = QuestionChoice.objects.get(id=question_choice_id.id)
                    except QuestionChoice.DoesNotExist:
                        continue 
                    new_question_choice_text = question_choice_data.get('optionText')
                    if question_choice_instance.question_choice != new_question_choice_text:
                        question_choice_instance.question_choice = new_question_choice_text
                        question_choice_instance.save()

                    options_to_create.append(QuestionChoiceSerializer(question_choice_instance).data)
        response_data = self.get_serializer(instance).data
        response_data['question'] = options_to_create

        return Response(response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)


class AnswersViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = Answers.objects.all().order_by('created_at')
    serializer_class = AnswersSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["answer","question","student"]


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)


class QuestionChoiceViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionChoice.objects.all().order_by('created_at')
    serializer_class = QuestionChoiceSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["question","question_choice"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"meassage":"Delete Successfully"},status=status.HTTP_200_OK)
