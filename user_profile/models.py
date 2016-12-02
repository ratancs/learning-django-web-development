from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user class.
    """
    username = models.CharField('username', max_length=10, unique=True, db_index=True)
    email = models.EmailField('email address', unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = u'user'

    def __unicode__(self):
        return self.username


class UserFollower(models.Model):
    user = models.ForeignKey(User, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    followers = models.ManyToManyField(User, related_name='followers')

    def __unicode__(self):
        return self.user.username


class Invitation(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=100)
    sender = models.ForeignKey(User)

    def __unicode__(self):
        return '%s, %s' % (self.sender.username, self.email)