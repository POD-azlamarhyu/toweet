from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404,JsonResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .serializers import *
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# @login_required
def tweetHomeView(request,*args,**kwargs):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request,"tweet/tweet.html",context={"username": username}, status=200)

@api_view(['GET'])
def tweetDetailView(request,tweet_id,*args,**kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=200)
    
    tweet = qs.first()
    serializer = TweetSerializer(tweet)
    return Response(serializer.data,status=200)

@api_view(['GET'])
def tweetListView(request,*args,**kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs,many=True)
    return Response(serializer.data,status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweetCreateView(request,*args,**kwargs):
    serializer = TweetCreateSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data,status=201)
    return Response({},status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweetEditView(request,tweet_id,*args,**kwargs):
    tweet = Tweet.objects.get(id=tweet_id)
    serializer = TweetSerializer(instance=tweet,data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data,status=201)
    
    return Response({},status=400)

@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def tweetDeleteView(request,tweet_id,*args,**kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)

    tweet = qs.first()
    tweet.delete()
    context = {
        "message":"Tweet removed"
    }
    return Response(context,status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweetLikeView(request,*args,**kwargs):
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id=data.get("id")
        action = data.get("action")
        text = data.get("text")
        print(data)
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({},status=404)

        tweet=qs.first()
        if action == "like":
            tweet.like.add(request.user)
            serializer = TweetSerializer(tweet)
            return Response(serializer.data,status=200)
        elif action == "unlike":
            tweet.like.remove(request.user)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                user = request.user,
                retweet = tweet,
                text = text,
            )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data,status=200)
    return Response({},status=200)

def tweetDetailViewDjango(request,tweet_id,*args,**kwargs):

    """
    Rest API View
    return json
    """

    # context = {
    #     "id" : tweet_id,
    # }

    # status = 200

    # try:
    #     tweet = Tweet.objects.get(id=tweet_id)
    #     context["text"] = tweet.text
    # except:
    #     context["message"] = "Not found"
    #     status = 404

    # return JsonResponse(context,status=status)


    """
    Dynamic Routing
    """
    try:
        tweet = Tweet.objects.get(id = tweet_id)
    except:
        raise Http404
    
    context = {
        "tweet" : tweet,
    }

    return render(request,'tweet/tweetdetail.html',context)

def tweetListViewDjango(request,*args,**kwargs):
    qs = Tweet.objects.all()
    #tweetList = [{"id" : x.id,"text":x.text} for x in qs]

    context = {
        "tweetlist" : qs
    }

    return render(request,"tweet/tweetlist.html",context)

def tweetCreateViewDjango(request,*args,**kwargs):

    user = request.user

    if not request.user.is_authenticated:
        if request.is_ajax():
            return JsonResponse({},status=401)

        return redirect(settings.LOGIN_URL)

    form = TweetForm()

    if request.method == "POST":
        form = TweetForm(request.POST)
        
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = user
            tweet.save()
        # messages.success(request,"投稿しました")
        
        return redirect('tweet:tweetlist')
    context = {
        "form" : form,
    }

    return render(request,"tweet/tweetcreate.html",context)

def tweetEditViewDjango(request,tweet_id,*args,**kwargs):

    tweet = Tweet.objects.get(id=tweet_id)
    form = TweetForm(instance=tweet)
    
    if request.method == "POST":
        form = TweetForm(request.POST,instance=tweet)
        if form.is_valid():
            form.save()
            # messages.success(request,"修正しました")
            # tweet.save()
            return redirect('tweet:tweetlist')
    
    context = {
        "form":form
    }

    return render(request,"tweet/tweetedit.html",context)

def tweetDeleteViewDjango(request,tweet_id,*args,**kwargs):
    tweet = Tweet.objects.get(id=tweet_id)

    if request.method == "POST":
        tweet.delete()

        return redirect('tweet:tweetlist')

    context = {
        "tweet":tweet,
        "tweet_id":tweet_id
    }

    return render(request,'tweet/tweetdelete.html',context)