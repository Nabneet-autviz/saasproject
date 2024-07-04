
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'user-list', CustomUserViewset, basename='quiz')

urlpatterns = [
    path('register', CustomApiView.as_view(), name='student-register'),
    path('login', LoginApiView.as_view(), name='student-login'),
    path('logout', LogoutApiView.as_view(), name='student-logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    ]+router.urls