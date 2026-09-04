from django import forms

from .models import ProfileUser


class ProfileForm(forms.ModelForm):

    class Meta:
        model = ProfileUser
        fields = ('avatar',)
