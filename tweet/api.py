from tastypie.resources import ModelResource
from tweet.models import Tweet, User
from tastypie.authentication import BasicAuthentication
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from django.http import HttpResponse
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse


class CORSResource(object):
    """
    Adds CORS headers to resources that subclass this.
    """
    def create_response(self, *args, **kwargs):
        response = super(CORSResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        allows = ','.join(map(unicode.upper, allowed))

        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method


class TweetResource(CORSResource, ModelResource):
    class Meta:
        queryset = Tweet.objects.all()
        resource_name = 'tweet'


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        authentication = BasicAuthentication()


class TaggedItemResource(ModelResource):
    content_object = GenericForeignKeyField({
        User: UserResource,
        Tweet: TweetResource
    }, 'content_object')

    class Meta:
        resource_name = 'user_tweet'
        queryset = User.objects.all()