from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import authentication, permissions
from .serializers import UserSerializer


class ListUsers(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
