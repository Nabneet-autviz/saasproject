from rest_framework import serializers
from .models import *
from authentication.models import ClassName

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"

class DifficultyRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DifficultyRating
        fields = "__all__"
class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = "__all__"

class QuestionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionGroup
        fields = "__all__"

class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = "__all__"

class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = "__all__"
class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    "related name use "
    question=QuestionChoiceSerializer(required=False,many=True)
    user_question=AnswersSerializer(required=False,many=True)
    # quiz_name = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    difficulty_rating  = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = "__all__"

    def get_quiz_name(self,obj):
        return obj.quizz.quiz_name
    def get_group_name(self,obj):
        return obj.questiongroup.questiongroup
    def get_difficulty_rating(self,obj):
        return obj.difficultyrating.difficultyrating
    def get_picture(self,obj):
        return PictureSerializer(obj.picture_question.all(),many=True).data
   
class UserQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class ClassNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassName
        fields = "__all__"