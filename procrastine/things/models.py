from django.db import models
from django.contrib.auth.models import User

class Thing(models.Model):
    TYPES = (
        (1, u'url'),
        (2, u'image'),
        (3, u'text')
    )

    owner = models.ForeignKey(User)
    content = models.CharField(max_length=510)
    type = models.IntegerField(choices=TYPES, default=3, blank=True)
    is_active = models.BooleanField('Active ?', default=True)

    def __unicode__(self):
        return self.url

    def delete(self):
        self.is_active = False
        self.save()

    def get_absolute_url(self):
        if self.pk:
            return reverse('things_view', args=[self.pk])
        return ''

