from datetime import datetime
import hashlib
import random
import string

from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save

class ProfileManager(models.Manager):
    def _generate_hash(self):
        salt = ''.join(random.choice(string.letters + string.digits) for x in range(10))
        return hashlib.sha1("%s#^)%s" % (salt, datetime.now().isoformat())).hexdigest()
    
    def create(self, **kwargs):
        return super(ProfileManager, self).create(key=self._generate_hash(), **kwargs)


class Profile(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=40)

    objects = ProfileManager()

    def __unicode__(self):
        if self.user:
            return u'%s profile' % self.user.username
        return u''


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

