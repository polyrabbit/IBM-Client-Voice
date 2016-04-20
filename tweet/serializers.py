# coding: utf-8
from __future__ import unicode_literals, absolute_import
import logging

from .models import Tweet, User
from rest_framework import serializers

logger = logging.getLogger(__name__)


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.CharField(source='get_user_mentions', read_only=True)

    class Meta:
        model = Tweet


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
