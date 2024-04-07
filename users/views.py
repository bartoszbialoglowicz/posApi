from django.shortcuts import render
from rest_framework import generics

from users import serializers

class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer