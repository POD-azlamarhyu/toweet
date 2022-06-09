from django.conf import settings
from rest_framework import serializers
from .models import *

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    text = serializers.CharField(allow_blank=True,required=False)
    print(text)
    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value

class TweetCreateSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'text', 'like','images','videos']
    def get_like(self, obj):
        return obj.like.count()
    
    def validate_text(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value
class TweetSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    retweet = TweetCreateSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'text', 'like','images','videos','is_retweet',"retweet"]
        
    def get_like(self, obj):
        return obj.like.count()
    
    # def get_text(self,obj):
    #     text = obj.text
    #     if obj.is_retweet:
    #         text = obj.retweet.text
    #     return obj.text
    


