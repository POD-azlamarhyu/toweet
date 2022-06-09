from django.db import models
from django.conf import settings
import random

User = settings.AUTH_USER_MODEL

class Tweet(models.Model):
    #id = models.AutoField(primary_key=True)
    retweet = models.ForeignKey("self",null=True,on_delete=models.SET_NULL)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tweet")
    text = models.CharField(max_length=500,blank=True,null=True)
    images = models.FileField(upload_to='images/',blank=True,null=True)
    videos = models.FileField(upload_to='videos/',blank=True,null=True)
    like = models.ManyToManyField(User,related_name='tweet_user',blank=True,through="Like",default=None)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    #timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.retweet != None


    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }

class Like(models.Model):

    tweet = models.ForeignKey("Tweet",on_delete=models.CASCADE,related_name="tweetlike")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userlike")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.tweet)
