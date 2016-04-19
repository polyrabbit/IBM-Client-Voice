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
    author = models.BigIntegerField()
    created_at = models.DateTimeField()
    text = models.CharField(max_length=200)
    user_mentions = ArrayField(models.BigIntegerField())
    hashtags = ArrayField(models.CharField(max_length=200))
    urls = ArrayField(models.URLField())

    def __unicode__(self):
        return self.text

    @classmethod
    def from_tweepy(cls, tweepy):
        if cls.objects.filter(id=tweepy.id).exists():
            return cls.objects.get(pk=tweepy.id)
        entities = tweepy.entities
        tweet_model = cls(id=tweepy.id,
                            author=tweepy.author.id,
                            created_at=pytz.UTC.localize(tweepy.created_at),
                            text=unescape(tweepy.text),
                            user_mentions=[u['id'] for u in entities['user_mentions']],
                            hashtags=[h['text'] for h in entities['hashtags']],
                            urls=[u['expanded_url'] for u in entities['urls']])
        tweet_model.save()
        return tweet_model