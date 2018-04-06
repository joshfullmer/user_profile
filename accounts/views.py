from django.contrib import messages
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm
)
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from . import forms
from . import models


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('home')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('home'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def user_profile(request):
    try:
        profile = models.UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        profile = None
    form = forms.UserProfileForm(instance=profile)
    if request.method == 'POST':
        form = forms.UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return HttpResponseRedirect('/accounts/profile/view/')
    return render(request, 'accounts/userprofile_form.html', {'form': form})


@login_required
def user_profile_detail(request):
    try:
        user_profile = models.UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user_profile = None
    return render(request,
                  'accounts/userprofile_detail.html',
                  {'user_profile': user_profile})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = forms.ChangePasswordForm(data=request.POST, request=request)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password successfully updated.")
                return HttpResponseRedirect('accounts/profile/view/')
            else:
                messages.error(request, "Old password incorrect.")
        else:
            messages.error(request, "Please correct the error below:")
    form = forms.ChangePasswordForm(request=request)
    return render(
        request,
        'accounts/change_password_form.html',
        {'form': form})
