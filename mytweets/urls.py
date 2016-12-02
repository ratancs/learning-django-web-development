from django.conf.urls import patterns, include, url

from django.contrib import admin

from tweet.views import Index, Profile, PostTweet, HashTagCloud, Search, SearchHashTag, HashTagJson, UserRedirect, MostFollowedUsers
from user_profile.views import Invite, InviteAccept, Register
from django.views.decorators.cache import cache_page
from tastypie.api import Api
from tweet.api import TweetResource, UserResource, TaggedItemResource

v1_api = Api(api_name='v1')
v1_api.register(TweetResource())
v1_api.register(UserResource())
v1_api.register(TaggedItemResource())

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Index.as_view()),
    url(r'^user/(\w+)/$', Profile.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^invite/$', Invite.as_view()),
    url(r'^invite/accept/(\w+)/$', InviteAccept.as_view()),
    url(r'^user/(\w+)/post/$', PostTweet.as_view()),
    url(r'^hashTag/(\w+)/$', HashTagCloud.as_view()),
    url(r'^search/$', Search.as_view()),
    url(r'^profile/$', UserRedirect.as_view()),
    url(r'^mostFollowed/$', MostFollowedUsers.as_view()),
    url(r'^search/hashTag$',  cache_page(60 * 15)(SearchHashTag.as_view())),
    url(r'^hashtag.json$', HashTagJson.as_view()),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^register/$', Register.as_view()),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^api/', include(v1_api.urls)),
)
