from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users import serializers

class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
