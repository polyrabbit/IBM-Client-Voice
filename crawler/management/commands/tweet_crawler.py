# coding: utf-8
from __future__ import unicode_literals, absolute_import
import json

from django.core.management import BaseCommand
from django.db.models import Max, Min
import tweepy
from tweet.models import Tweet
import pytz

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

    def add_arguments(self, parser):
        parser.add_argument('historical', nargs='+', type=int)

    def handle(self, *args, **options):
        if 'historical' in args:
            return self.historical_update()
        since_id = Tweet.objects.filter().aggregate(max_id=Max('id')).get('max_id') or 1
        public_tweets = tweepy.Cursor(api.user_timeline, id='IBMclientvoices', since_id=since_id).items()
        self.save_tweet(public_tweets)

    def historical_update(self):
        oldest_id = Tweet.objects.filter().aggregate(min_id=Min('id')).get('min_id') or 0
        public_tweets = tweepy.Cursor(api.user_timeline, id='IBMclientvoices', max_id=oldest_id).items()
        self.save_tweet(public_tweets)

    def save_tweets(self, public_tweets):
        for tweet in public_tweets:
            if Tweet.objects.filter(id=tweet.id).exists():
                return
            entities = tweet.entities
            tweet_model = Tweet(id=tweet.id,
                                author=tweet.author.id,
                                created_at=pytz.UTC.localize(tweet.created_at),
                                text=tweet.text,
                                user_mentions=[u['id'] for u in entities['user_mentions']],
                                hashtags=[h['text'] for h in entities['hashtags']],
                                urls=[u['expanded_url'] for u in entities['urls']])
            tweet_model.save()
            print tweet.text.encode('utf8')