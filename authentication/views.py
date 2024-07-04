from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import *
from .serializers import *
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework import status, viewsets
# from quizapp.pagination import *


# Create your views here.

class CustomApiView(APIView):
    permission_classes = [AllowAny] 
    def post(self,request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        error_keys = list(serializer.errors.keys()) if isinstance(serializer.errors, dict) else []  
        error_keys_str = ', '.join(error_keys)
        return Response({"message":error_keys_str + " is already exists"}, status=status.HTTP_400_BAD_REQUEST)
    

class LoginApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
    
            return JsonResponse(
                {
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'user_info':CustomUserSerializer(user,many=False).data
                }
            )
        return Response({'message':"username or password are incorrect"})

class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    def post(self, request):
        print(request.data)
        
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)},status=status.HTTP_400_BAD_REQUEST)



class CustomUserViewset(viewsets.ModelViewSet):
    Permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(is_staff=False)
    serializer_class = CustomUserSerializer
    # pagination_class = CustomPagination

from rest_framework_simplejwt.views import TokenRefreshView

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

