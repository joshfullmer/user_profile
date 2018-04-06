from django import forms
from tinymce.widgets import TinyMCE

from . import models
from .constants import PASSWORD_HELP_TEXT, PASSWORD_SPEC_CHARS


class UserProfileForm(forms.ModelForm):
    email2 = forms.EmailField(label='Confirm email address')
    bio = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = models.UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'email2',
            'date_of_birth',
            'bio',
            'avatar',
            'hobbies',
            'city',
            'state',
            'country',
        ]

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
        if cleaned_data['email'] != cleaned_data['email2']:
            raise forms.ValidationError("Email addresses don't match")
        if len(cleaned_data['bio']) < 10:
            raise forms.ValidationError(
                "Bio must be longer than 10 characters")
        return cleaned_data


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(help_text=PASSWORD_HELP_TEXT,
                                   widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Confirm new password',
                                    widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data['new_password']
        if cleaned_data['old_password'] == password:
            raise forms.ValidationError(
                "New password cannot match old password")
        if password != cleaned_data['new_password2']:
            raise forms.ValidationError(
                "New passwords don't match")
        if len(password) < 14:
            raise forms.ValidationError(
                "Password must be at least 14 characters")
        if not any(letter.isupper() for letter in password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter")
        if not any(letter.islower() for letter in password):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter")
        if not any(letter.isdigit() for letter in password):
            raise forms.ValidationError(
                "Password must contain at least one digit (0-9)")
        if not any(letter in PASSWORD_SPEC_CHARS for letter in password):
            raise forms.ValidationError(
                "Password must contain at least special character")
        try:
            profile = self.request.user.profile
        except models.UserProfile.DoesNotExist:
            pass
        else:
            if (profile.first_name.lower() in password.lower() or
                    profile.last_name.lower() in password.lower()):
                raise forms.ValidationError(
                    "Password cannot contain your first or last name")

        return cleaned_data
