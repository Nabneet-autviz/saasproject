
from django.urls import path
from .views import *

urlpatterns = [
    path('register', CustomApiView.as_view(), name='student-register'),
    path('login', LoginApiView.as_view(), name='student-login'),
    path('logout', LogoutApiView.as_view(), name='student-logout'),
    path(
        "user-list/",
        CustomUserViewset.as_view({"get": "list"}),
        name="user_list",
    ),
    ]