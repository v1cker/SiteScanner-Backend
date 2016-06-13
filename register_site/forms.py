from django import forms
from .models import EntriesIndex, WatchersIndex, RedirectionsIndex


class EntriesIndexForm(forms.ModelForm):
    class Meta:
        model = EntriesIndex
        fields = ['alias', 'url']


class WatchersIndexForm(forms.ModelForm):
    class Meta:
        model = WatchersIndex
        fields = ['title', 'description', 'h1']


class RedirectionsIndexForm(forms.ModelForm):
    class Meta:
        model = RedirectionsIndex
        fields = ['target_url', 'status_code']
