from django.db import models
from django.contrib.auth.models import User

class Link(models.Model):
    owner = models.ForeignKey(User)
    url = models.URLField(verify_exists=True)
    is_active = models.BooleanField('Active ?', default=True)

    def __unicode__(self):
        return self.url

    def delete(self):
        self.is_active = False
        self.save()

    def get_absolute_url(self):
        return self.url

