from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
# from .pagination import *
from django_filters.rest_framework import DjangoFilterBackend
import json
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.http import QueryDict
from authentication.models import *
# Create your views here.


class QuizViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = Quiz.objects.all().order_by('-created_at')
    serializer_class = QuizSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["quiz_name","quiz_description","difficultyrating"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance_data = serializer.data
        self.perform_destroy(instance)
        return Response({"message": "Delete Successfully", "deleted_instance": instance_data}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.delete()

class DifficultyRatingViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = DifficultyRating.objects.all().order_by('-created_at')
    serializer_class = DifficultyRatingSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["difficultyrating"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance_data = serializer.data
        self.perform_destroy(instance)
        return Response({"message": "Delete Successfully", "deleted_instance": instance_data}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.delete()


class QuestionGroupViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionGroup.objects.all().order_by('-created_at')
    serializer_class = QuestionGroupSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["questiongroup"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance_data = serializer.data
        self.perform_destroy(instance)
        return Response({"message": "Delete Successfully", "deleted_instance": instance_data}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.delete()


class QuestionTypeViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionType.objects.all().order_by('-created_at')
    serializer_class = QuestionTypeSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["questiontype"]


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance_data = serializer.data
        self.perform_destroy(instance)
        return Response({"message": "Delete Successfully", "deleted_instance": instance_data}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.delete()


class QuestionViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["quizz","difficultyrating","questiongroup","questiontype","user_question__student"]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        parser_classes = (MultiPartParser, FormParser, JSONParser)
        questions = request.data.get('questions')
        if isinstance(questions, list):
            questions = questions[0] 

        if questions:
            try:
                questions_data = json.loads(questions)
            except json.JSONDecodeError as e:
                return Response({"error": f"Invalid JSON data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No questions data provided"}, status=status.HTTP_400_BAD_REQUEST)

        response_data = []
        for index,question_data in enumerate(questions_data):

            question_dict = {
                'content': question_data['content'],
                'answer': question_data['answer'],
                'difficultyrating': int(question_data['difficultyrating']),
                'quizz': question_data['quizz'],
                'questiontype': question_data['questiontype'],
                'questiongroup': question_data['questiongroup'],
                'comment':question_data['comment']
            }
            serializer = self.get_serializer(data=question_dict)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            question_id = serializer.instance.id
            pictures_key = f'pictures-{index}'
            image_data = []
            if pictures_key in request.FILES:
                for file in request.FILES.getlist(pictures_key):
                    data_img = {"question": question_id, "picture": file}
                    image_data.append(data_img)
            if image_data:
                picture_serializer = PictureSerializer(data=image_data, many=True)
                picture_serializer.is_valid(raise_exception=True)
                picture_serializer.save()
            options_data = []
            for option_data in question_data['options']:
                option_dict = {
                    'question': question_id,
                    'question_choice': option_data['optionText']
                }
                options_data.append(option_dict)
            if options_data:
                option_serializer = QuestionChoiceSerializer(data=options_data, many=True)
                option_serializer.is_valid(raise_exception=True)
                option_serializer.save()
                response_data.append(serializer.data)
        
        return Response(response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        parser_classes = (MultiPartParser, FormParser, JSONParser)
        questions = request.data.get('questions')
        if isinstance(questions, list):
            questions = questions[0]  

        if questions:
            try:
                questions_data = json.loads(questions)
            except json.JSONDecodeError as e:
                return Response({"error": f"Invalid JSON data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No questions data provided"}, status=status.HTTP_400_BAD_REQUEST)
        question_data = data.get('question', {})
        response_data = []
        for index,question_data in enumerate(questions_data):
            question_dict = {
                'content': question_data.get('content', instance.content),
                'answer': question_data.get('answer', instance.answer),
                'difficultyrating': question_data.get('difficultyrating', instance.difficultyrating),
                'quizz': question_data.get('quizz', instance.quizz),
                'questiontype': question_data.get('questiontype', instance.questiontype),
                'questiongroup': question_data.get('questiongroup', instance.questiongroup),
                'comment':question_data.get('comment',instance.comment)
            }
            serializer = self.get_serializer(instance, data=question_dict, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            question_id = serializer.instance.id
            pictures_key = f'pictures-{index}'
            image_data = []
            if pictures_key in request.FILES:
                for file in request.FILES.getlist(pictures_key):
                    data_img = {"question": question_id, "picture": file}
                    image_data.append(data_img)
            if image_data:
                picture_serializer = PictureSerializer(data=image_data, many=True)
                picture_serializer.is_valid(raise_exception=True)
                picture_serializer.save()
            options_data = question_data.get('options', [])
            options_to_create = []
            for question_choice_data in options_data:
                question_choice_id = question_choice_data.get('id')
                new_question_choice_text = question_choice_data.get('optionText')

                if question_choice_id is not None:
                    try:
                        question_choice_instance = QuestionChoice.objects.get(id=question_choice_id)
                    except QuestionChoice.DoesNotExist:
                        continue

                    if question_choice_instance.question_choice != new_question_choice_text:
                        question_choice_instance.question_choice = new_question_choice_text
                        question_choice_instance.save()

                    options_to_create.append(QuestionChoiceSerializer(question_choice_instance).data)
                elif new_question_choice_text:
                    new_question_choice_instance = QuestionChoice.objects.create(question_id=question_id,question_choice=new_question_choice_text)
                    options_to_create.append(QuestionChoiceSerializer(new_question_choice_instance).data)
            if 'optionDeleteIds' in question_data: 
                QuestionChoice.objects.filter(id__in=question_data['optionDeleteIds']).delete()
            else:
                pass        
            if 'pictureDeleteIds' in question_data:
                Picture.objects.filter(id__in=question_data['pictureDeleteIds']).delete()
            else:
                pass
            response_data = self.get_serializer(instance).data
            response_data['options'] = options_to_create

            return Response(response_data, status=status.HTTP_200_OK)

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance_data = serializer.data
        self.perform_destroy(instance)
        return Response({"message": "Delete Successfully", "deleted_instance": instance_data}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.delete()

class AnswersViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = Answers.objects.all().order_by('-created_at')
    serializer_class = AnswersSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["answer","question","student"]


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance_data = serializer.data
        self.perform_destroy(instance)
        return Response({"message": "Delete Successfully", "deleted_instance": instance_data}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.delete()


class QuestionChoiceViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = QuestionChoice.objects.all().order_by('-created_at')
    serializer_class = QuestionChoiceSerializer
    # pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["question","question_choice"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance_data = serializer.data
        self.perform_destroy(instance)
        return Response({"message": "Delete Successfully", "deleted_instance": instance_data}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.delete()


class PictureViewset(viewsets.ModelViewSet):
    permission_classes= [IsAuthenticated]
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class ClassNameViewset(viewsets.ModelViewSet):
    queryset = ClassName.objects.all()
    serializer_class = ClassNameSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance_data = serializer.data
        self.perform_destroy(instance)
        return Response({"message": "Delete Successfully", "deleted_instance": instance_data}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.delete()




class UserQuizViewset(APIView):
    queryset = Answers.objects.all()
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch data from the database
        data = Answers.objects.filter(student__id=user_id).values(
            'question__questiongroup__quizz__id',
            'question__questiongroup__quizz__quiz_name',
            'question__questiongroup__id',
            'question__questiongroup__questiongroup'
        )
        
        # Process data into the desired dictionary structure
        quiz_dict = {}
        
        for entry in data:
            quiz_id = entry['question__questiongroup__quizz__id']
            quiz_name = entry['question__questiongroup__quizz__quiz_name']
            question_group_id = entry['question__questiongroup__id']
            question_group_name = entry['question__questiongroup__questiongroup']
            
            if quiz_id not in quiz_dict:
                quiz_dict[quiz_id] = {
                    "id": quiz_id,
                    "quiz_name": quiz_name,
                    "quizGroup": []
                }
            
            # Avoid adding duplicate question groups
            if not any(qg['questiongroupid'] == question_group_id for qg in quiz_dict[quiz_id]["quizGroup"]):
                quiz_dict[quiz_id]["quizGroup"].append({
                    "questiongroupid": question_group_id,
                    "questiongroup": question_group_name
                })
        
        # Sort each quizGroup by questiongroupid
        for quiz in quiz_dict.values():
            quiz["quizGroup"] = sorted(quiz["quizGroup"], key=lambda x: x["questiongroupid"])
        
        # Convert quiz_dict to a list and sort quizzes by id (if needed)
        quizzes = sorted(quiz_dict.values(), key=lambda x: x["id"])
        
        return Response(quizzes, status=status.HTTP_200_OK)
    

class UserQuestionAnswer(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        question_group = request.query_params.get('questiongroup')
        if not question_group:
            return Response({"error": "questiongroup parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        questions = Question.objects.filter(questiongroup=question_group)
        ser_data = UserQuestionAnswerSerializer(questions, many=True)

        custom_data = []
        for item in ser_data.data:
            question_entry = {
                "id": item['id'],
                "content": item['content'],
                "admin_answer": item['answer'],
                "quizz": item['quizz'],
                "difficultyrating": item['difficultyrating'],
                "questiongroup": item['questiongroup'],
                "questiontype": item['questiontype']
            }

            # Add user data
            answers = Answers.objects.filter(question__id=item['id'])
            answers_serialized = AnswersSerializer(answers, many=True).data
            
            if answers_serialized:
                answer_content = json.loads(answers_serialized[0]['answer'])  
                user_answer = answer_content[0]['question_choice'] if answer_content else None

                user_data = {
                    "id": answers_serialized[0]['id'],
                    "user_answer": user_answer,
                    "question_id": item['id'],
                    "studentid": answers_serialized[0]['student'],
                    "updated_at": answers_serialized[0]['updated_at'],
                    "created_date": answers_serialized[0]['created_at']
                }
                question_entry["user_data"] = user_data

            custom_data.append(question_entry)

        return Response({"message": "Data retrieved successfully", "data": custom_data}, status=status.HTTP_200_OK)
    



# class UserResultdata(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self,request):
#         user_id = request.query_params.get('user_id')
#         data = Answers.objects.filter(student__id=user_id)
#         for ans in data:
#             # i.question.id==Question.objects.filter(id=119)
#             # Each ans holds a JSON-like structure
#             response_data = json.loads(str(ans))  # Convert the Answers object to a string and load it
#             for item in response_data:
#                 print(item['question_choice'])
#                 print(item['question'])
                