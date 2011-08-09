from django import forms

from links.models import Link

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link

