from django.urls import path
from .views import *

app_name = "tweet"

urlpatterns = [
    path('tweet',tweetHomeView,name="tweethome"),
    path('tweets/<int:tweet_id>',tweetDetailView,name="tweetdetail"),
    path('tweets',tweetListView,name="tweetlist"),
    path('tweets/create',tweetCreateView,name="tweetcreate"),
    path('tweets/edit/<int:tweet_id>',tweetEditView,name="tweetedit"),
    path('tweets/delete/<int:tweet_id>',tweetDeleteView,name="tweetdelete"),
    path('tweets/like',tweetLikeView,name="tweetlike"),
    path('tweetdjango/',tweetListViewDjango,name="tweetlistdjango"),
    path('tweetcreatedjango/',tweetCreateViewDjango,name="tweetcreatedjango"),
    path('tweeteditdjango/<int:tweet_id>',tweetEditViewDjango,name="tweeteditdjango"),
    path('tweetdeletedjango/<int:tweet_id>',tweetDeleteViewDjango,name="tweetdeletedjango"),
    path('tweetdetaildjango/<int:tweet_id>',tweetDetailViewDjango,name="tweetdetaildjango"),
]