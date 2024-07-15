from rest_framework import serializers
from .models import *
from quizapp.models import Answers
from django.db.models import Count
from quizapp.serializers import ClassNameSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class_name=serializers.SerializerMethodField()
    quiz_count = serializers.SerializerMethodField()
      
    class Meta:
        model =CustomUser
        fields="__all__"
        fields = ('id','username', 'password', 'email', 'first_name', 'last_name','created_at','updated_at','class_name','quiz_count')

    def get_quiz_count(self,obj):
        return Answers.objects.filter(student=obj).values(
            'question__questiongroup__quizz__id'
        ).annotate(quiz_count=Count('question__questiongroup__quizz__id')).count()
    def get_class_name(self,obj):
        return obj.class_name.class_name if obj.class_name else None
    
    
class CustomUserSignSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  
    class Meta:
        model =CustomUser
        fields="__all__"
        fields = ('id','username', 'password', 'email', 'first_name', 'last_name','created_at','updated_at','class_name')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)

        return user
    
