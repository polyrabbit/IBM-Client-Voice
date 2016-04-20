# coding: utf-8
from __future__ import unicode_literals, absolute_import
import logging

from django.views.generic import TemplateView
from rest_framework import viewsets
from .models import Tweet, User
from .serializers import TweetSerializer, UserSerializer

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'


class TweetViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = TweetSerializer

    def get_queryset(self):
        return Tweet.objects.filter(text__icontains=self.request.GET.get('text', '')).order_by('-id')


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
