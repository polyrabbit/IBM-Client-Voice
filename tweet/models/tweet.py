# coding: utf-8
from __future__ import unicode_literals, absolute_import
import logging

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

logger = logging.getLogger(__name__)

class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    author = models.BigIntegerField()
    created_at = models.DateTimeField()
    text = models.CharField(max_length=200)
    user_mentions = ArrayField(models.BigIntegerField())
    hashtags = ArrayField(models.CharField(max_length=200))
    urls = ArrayField(models.URLField())

    def __str__(self):
        return self.text.encode('utf-8')