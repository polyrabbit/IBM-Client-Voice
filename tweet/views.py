# coding: utf-8
from __future__ import unicode_literals, absolute_import
import logging

from django.views.generic import TemplateView
from rest_framework import viewsets
from .models import Tweet, User
from .serializers import TweetSerializer, UserSerializer

logger = logging.getLogger(__name__)


class TemplateProvider(TemplateView):

    def get_template_names(self):
        return [self.kwargs['template']+'.html']


class TweetViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = TweetSerializer

    def get_queryset(self):
        queryset = Tweet.objects.order_by('-id')
        params = self.request.GET
        if 'text' in params:
            queryset = queryset.filter(text__icontains=params.get('text', ''))
        if 'hashtags' in params:
            queryset = queryset.filter(hashtags__contains=params.getlist('hashtags', []))
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
