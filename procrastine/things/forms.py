import re

from django import forms

from things.models import Thing

class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing

    def clean(self):
        cleaned_data = super(ThingForm, self).clean()
        types = dict((k, v) for v, k in Thing.TYPES)
        content = cleaned_data.get('content', '')
        # Is URL
        if re.match(r'^https?:\/\/', content):
            cleaned_data.update({'type': types['url']})
        # Treat as text
        else:
            cleaned_data.update({'type': types['text']})
        return cleaned_data

