from django import forms

from . import models


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'bio',
            'avatar',
            'hobbies',
            'city',
            'state',
            'country',
        ]
