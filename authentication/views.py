from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import SignInSerializer, SignupSerailizer
import random

# Create your views here.


class SignupView(APIView):
    
    def post(self, request):
        
        try:
            
            serializer = SignupSerailizer(data=request.data)
            
            if not serializer.is_valid():
                return Response(serializer.errors)
            
            user_qs = User.objects.filter(email=request.data['email']).exists()
            
            if user_qs:
                return Response({"message":"email already exists"})
            else:
                
                username = request.data['name'] + str(random.randint(100, 999))
                
                user = User(
                    username=username,
                    email=serializer.validated_data['email'],
                    display_name=serializer.validated_data['name']
                )
                user.set_password(serializer.validated_data['password'])
                user.save()
            
            return Response({"message":"user created successfully"})
        except Exception as e:
            print(str(e))

class SignInView(APIView):
    
    def post(self, request):
        
        try:
            
            serializer = SignInSerializer(data=request.data)
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            print(str(e))