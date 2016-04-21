# coding: utf-8
from __future__ import unicode_literals, absolute_import
import logging
import HTMLParser

import pytz
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

logger = logging.getLogger(__name__)


html_parser = HTMLParser.HTMLParser()
unescape = html_parser.unescape


class Tweet(models.Model):
    class Meta:
        db_table = 'tweet'
        ordering = ['-id']

    id = models.BigIntegerField(primary_key=True)
    author = models.ForeignKey('User')
    created_at = models.DateTimeField()
    text = models.CharField(max_length=200)
    user_mentions = ArrayField(models.BigIntegerField())
    hashtags = ArrayField(models.CharField(max_length=200), default=list)
    media_urls = ArrayField(models.URLField(), default=list)
    urls = ArrayField(models.URLField(), default=list)

    def __unicode__(self):
        return self.text

    @classmethod
    def from_tweepy(cls, tweepy):
        if cls.objects.filter(id=tweepy.id).exists():
            return cls.objects.get(pk=tweepy.id)
        entities = tweepy.entities
        tweet_obj = cls(id=tweepy.id,
                            author_id=tweepy.author.id,
                            created_at=pytz.UTC.localize(tweepy.created_at),
                            text=unescape(tweepy.text),
                            user_mentions=[u['id'] for u in entities['user_mentions']] if 'user_mentions' in entities else [],
                            hashtags=[h['text'] for h in entities['hashtags']] if 'hashtags' in entities else [],
                            media_urls=[m['media_url'] for m in entities['media']] if 'media' in entities else [],
                            urls=[u['expanded_url'] for u in entities['urls']] if 'urls' in entities else [])
        tweet_obj.save()
        return tweet_obj

    @property
    def users(self):
        from .user import User
        return User.objects.filter(id__in=self.user_mentions)
