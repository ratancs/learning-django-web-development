from django.views.generic import View,TemplateView
from django.shortcuts import render
from user_profile.models import User, UserFollower
from models import Tweet, HashTag
from tweet.forms import TweetForm, SearchForm, SearchHashTagForm
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.template import Context
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import logging
logger = logging.getLogger('django')

TWEET_PER_PAGE = 5


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class Index(View):
    def get(self, request):
        params = dict()
        params["name"] = "Django"
        return render(request, 'base.html', params)


class UserRedirect(View):
    def get(self, request):
        if request.user.is_authenticated():
            logger.info('authorized user')
            return HttpResponseRedirect('/user/'+request.user.username)
        else:
            logger.info('unauthorized user')
            return HttpResponseRedirect('/login/')


class MostFollowedUsers(View):
    def get(self, request):
        userFollowers = UserFollower.objects.order_by('-count')[:2]
        params = dict()
        params['userFollowers'] = userFollowers
        return render(request, 'users.html', params)


class Profile(LoginRequiredMixin, View):
    """User Profile page reachable from /user/<username> URL"""
    def get(self, request, username):
        params = dict()
        userProfile = User.objects.get(username=username)
        try:
            userFollower = UserFollower.objects.get(user=userProfile)
            if userFollower.followers.filter(username=request.user.username).exists():
                params["following"] = True
            else:
                params["following"] = False
        except:
            userFollower = []

        form = TweetForm(initial={'country': 'Global'})
        search_form = SearchForm()
        tweets = Tweet.objects.filter(user=userProfile).order_by('-created_date')
        paginator = Paginator(tweets, TWEET_PER_PAGE)
        page = request.GET.get('page')
        try:
            tweets = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tweets = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            tweets = paginator.page(paginator.num_pages)

        params["tweets"] = tweets
        params["profile"] = userProfile
        params["form"] = form
        params["search"] = search_form
        return render(request, 'profile.html', params)

    def post(self, request, username):
        follow = request.POST['follow']
        user = User.objects.get(username= request.user.username)
        userProfile = User.objects.get(username=username)
        userFollower, status = UserFollower.objects.get_or_create(user=userProfile)
        userFollower.count += 1
        userFollower.save()
        if follow == 'true':
            #follow user
            userFollower.followers.add(user)
        else:
            #unfollow user
            userFollower.followers.remove(user)
        return HttpResponse(json.dumps(""), content_type="application/json")



class PostTweet(View):
    """Tweet Post form available on page /user/<username> URL"""
    def post(self, request, username):
        form = TweetForm(self.request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            tweet = Tweet(text=form.cleaned_data['text'],
                                         user=user,
                                         country=form.cleaned_data['country'])
            tweet.save()
            words = form.cleaned_data['text'].split(" ")
            for word in words:
                if word[0] == "#":
                    hashtag, created = HashTag.objects.get_or_create(name=word[1:])
                    hashtag.tweet.add(tweet)
        return HttpResponseRedirect('/user/'+username)


class HashTagCloud(View):
    """Hash Tag  page reachable from /hashTag/<hashtag> URL"""
    def get(self, request, hashtag):
        params = dict()
        hashtag = HashTag.objects.get(name=hashtag)
        params["tweets"] = hashtag.tweet
        return render(request, 'hashtag.html', params)


class Search(View):
    """Search all tweets with query /search/?query=<query> URL"""
    def get(self, request):
        form = SearchForm()
        params = dict()
        params["search"] = form
        return render(request, 'search.html', params)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            tweets = Tweet.objects.filter(text__icontains=query)
            context = Context({"query": query, "tweets": tweets})
            return_str = render_to_string('partials/_tweet_search.html', context)
            return HttpResponse(json.dumps(return_str), content_type="application/json")
        else:
            HttpResponseRedirect("/search")


class SearchHashTag(View):
    """Search a hashTag with auto complete feature"""
    def get(self, request):
        form = SearchHashTagForm()
        params = dict()
        params["search"] = form
        return render(request, 'search_hashtag.html', params)

    def post(self, request):
        params = dict()
        query = request.POST['query']
        form = SearchHashTagForm()
        hashtags = HashTag.objects.filter(name__contains=query)
        params["hashtags"] = hashtags
        params["search"] = form
        return render(request, 'search_hashtag.html', params)


class HashTagJson(View):
    """Search a hashTag with auto complete feature"""
    def get(self, request):
        query = request.GET['query']
        hashtaglist = []
        hashtags = HashTag.objects.filter(name__icontains=query)
        for hashtag in hashtags:
            temp = dict()
            temp["query"] = (hashtag.name)
            hashtaglist.append(temp)
        return HttpResponse(json.dumps(hashtaglist), content_type="application/json")