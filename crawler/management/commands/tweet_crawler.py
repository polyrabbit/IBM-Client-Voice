# coding: utf-8
from __future__ import unicode_literals, absolute_import
import json

from django.core.management import BaseCommand
import tweepy
from tweet.models import Tweet

consumer_key = 'xocke92ayr1SCD2n0MMX3jkPI'
consumer_secret = 'JA22R5GvyBSo05yE6WGB1RtVJupEMp8H46qcSiq02hfe00i93v'
access_token = '988082462-QyPpRlMiW9PDHTAV1PfT78BmvXxrCYIn0WpRL0UP'
access_token_secret = 'R5TphLdzGxExej9gCGeqOsMAJcPIQg0jBFkCA9QFM8GGe'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class Command(BaseCommand):

    can_import_settings = True
    help = "Crawl tweet of IBM Client Voices, parse it and store to DB"

    def handle(self, *args, **options):
        public_tweets = api.user_timeline(id='IBMclientvoices', count=2)
        for tweet in public_tweets:
            entities = tweet.entities
            tweet_model = Tweet(id=tweet.id,
                                author=tweet.author.id,
                                created_at=tweet.created_at,
                                text=tweet.text,
                                user_mentions=[u['id'] for u in entities['user_mentions']],
                                hashtags=[h['text'] for h in entities['hashtags']],
                                urls=[u['expanded_url'] for u in entities['urls']])
            tweet_model.save()
            print json.dumps(tweet._json, indent=2, ensure_ascii=False).encode('utf8')
            print