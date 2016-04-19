# coding: utf-8
from __future__ import unicode_literals, absolute_import
import logging

from rest_framework import viewsets
from .models import Tweet, User
from .serializers import TweetSerializer, UserSerializer

logger = logging.getLogger(__name__)


class TweetViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Tweet.objects.all().order_by('-id')
    serializer_class = TweetSerializer


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
