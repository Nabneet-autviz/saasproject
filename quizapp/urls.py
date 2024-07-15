
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register(r'quiz', QuizViewset, basename='quiz')
router.register(r'difficulity-rating', DifficultyRatingViewset, basename='difficulity')
router.register(r'question-group', QuestionGroupViewset, basename='question_group')
router.register(r'question-type', QuestionTypeViewset, basename='question_type')
router.register(r'question', QuestionViewset, basename='question')
router.register(r'answer', AnswersViewset, basename='answer')
router.register(r'question-choice', QuestionChoiceViewset, basename='question_choice')
router.register(r'pictue', PictureViewset, basename='picture')
router.register(r'class-name', ClassNameViewset, basename='class_name')

urlpatterns = [path('user-quiz/', UserQuizViewset.as_view(), name='user_quiz'),
               path('user-question/', UserQuestionAnswer.as_view(), name='user_question')]+router.urls
            #    path('user-result-data/', UserResultdata.as_view(), name='user_result_data')]
            