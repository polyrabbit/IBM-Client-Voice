# coding: utf-8
from __future__ import unicode_literals, absolute_import
import time

from django.core.management import BaseCommand
from django.db.models import Max, Min
import tweepy
from tweet.models import Tweet, User

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
        parser.add_argument("--older", action="store_true", dest="older", default=False)

    def handle(self, *args, **options):
        if options.get('older'):
            return self.update_older()
        return self.update_newer()

    def update_newer(self):
        since_id = Tweet.objects.filter().aggregate(max_id=Max('id')).get('max_id') or 10000
        public_tweets = api.user_timeline(id='IBMclientvoices', since_id=since_id, count=20)
        if public_tweets:
            self.save_tweets(public_tweets)
            time.sleep(2)  # Pause for Rate Limitation
            self.update_newer()

    def update_older(self):
        oldest_id = Tweet.objects.filter().aggregate(min_id=Min('id')).get('min_id')
        if not oldest_id:
            public_tweets = api.user_timeline(id='IBMclientvoices')
        else:
            public_tweets = api.user_timeline(id='IBMclientvoices', count=20, max_id=oldest_id-1)
        if public_tweets:
            self.save_tweets(public_tweets)
            self.update_older()

    def save_tweets(self, public_tweets):
        for tweet in public_tweets:
            User.from_tweepy(tweet.author)
            for u in tweet.entities['user_mentions']:
                User.from_dict(u, api.get_user)
            Tweet.from_tweepy(tweet)
            print tweet.text.encode('utf8')
