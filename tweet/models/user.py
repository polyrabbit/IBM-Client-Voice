# coding: utf-8
from __future__ import unicode_literals, absolute_import
import logging

from tweepy.error import TweepError
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

logger = logging.getLogger(__name__)

class User(models.Model):
    class Meta:
        db_table = 'tweet_user'
        ordering = ['-id']

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    profile_image_url = models.URLField()
    lang = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    followers_count = models.IntegerField(default=int)
    urls = ArrayField(models.URLField(), default=list)

    def __unicode__(self):
        return self.name

    @classmethod
    def from_tweepy(cls, tweepy):
        if cls.objects.filter(id=tweepy.id).exists():
            return cls.objects.get(pk=tweepy.id)
        try:
            urls = [u['expanded_url'] for u in tweepy.entities['url']['urls']]
        except KeyError:
            urls = []
        user = cls(id=tweepy.id,
            name=tweepy.name,
            description=tweepy.description,
            profile_image_url=tweepy.profile_image_url,
            lang=tweepy.lang,
            location=tweepy.location,
            followers_count=tweepy.followers_count,
            urls=urls)
        user.save()
        return user

    @classmethod
    def from_dict(cls, user_dict, make_tweepy):
        if cls.objects.filter(id=user_dict['id']).exists():
            return cls.objects.get(pk=user_dict['id'])
        try:
            return cls.from_tweepy(make_tweepy(id=user_dict['id']))
        except TweepError as e:
            u = cls(id=user_dict['id'],
                    name=user_dict.get('name'))
            u.save()
            return u