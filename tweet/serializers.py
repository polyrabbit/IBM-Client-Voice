# coding: utf-8
from __future__ import unicode_literals, absolute_import
import logging

from .models import Tweet, User
from rest_framework import serializers

logger = logging.getLogger(__name__)


class UserField(serializers.RelatedField):
    def to_representation(self, value):
        return UserSerializer(value).data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class TweetSerializer(serializers.ModelSerializer):
    users = UserField(many=True, read_only=True)

    class Meta:
        model = Tweet
        depth = 1
