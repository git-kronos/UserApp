from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm,
                                       UserCreationForm)
from django.contrib.auth.models import User, UserCreationForm
from django.forms import ModelForm, fields

from .models import UserProfile, UserToken, country_list


class UserForm(UserCreationForm):
    """
    Form that uses built-in UserCreationForm to handle user creation
    """
    first_name = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput(
            attrs={
                'placeholder': '*Your first name..',
                'class': 'form-control form-control-lg'
            }))
    last_name = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput(
            attrs={
                'placeholder': '*Your last name..',
                'class': 'form-control form-control-lg'
            }))
    username = forms.EmailField(
        max_length=254, required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': '*Email...',
                'class': 'form-control form-control-lg'
            }))
    password1 = forms.CharField(
        max_length=254, required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '*Password...',
                'class': 'form-control form-control-lg password'
            }))
    password2 = forms.CharField(
        max_length=254, required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '*Re-enter Password...',
                'class': 'form-control form-control-lg password'
            }))
    token = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name',
            'password1', 'password2', 'captcha',
        )


class UserEmailForm(forms.ModelForm):
    """
    Form that uses built-in UserCreationForm to handle user creation
    """
    email = forms.EmailField(
        max_length=254, required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': '*Email...',
                'class': 'form-control'
            }))
    class Meta:
        model = User
        fields = ('email',)


class UserAlterationForm(forms.ModelForm):
    """
    Form that uses built-in UserCreationForm to handle user creation
    """
    first_name = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput(
            attrs={
                'placeholder': '*Your first name..',
                'class': 'form-control'
            }))
    last_name = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput(
            attrs={
                'placeholder': '*Your last name..',
                'class': 'form-control'
            }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class AuthForm(AuthenticationForm):
    """
    Form that uses built-in AuthenticationForm to handle user creation
    """
    username = forms.EmailField(
        max_length=254, required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': '*Email...',
                'class': 'form-control form-control-lg'
            }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '*Password...',
                'class': 'form-control form-control-lg password'
            }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(UserCreationForm):
    """
    Form that uses built-in UserCreationForm to handle user creation
    """
    telephone = forms.CharField(
        max_length=15, required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': '*Telephone...',
                'class': 'form-control'
            }))
    address = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput(
            attrs={
                'placeholder': '*First line of address...',
                'class': 'form-control'
            }))

    class Meta:
        model = UserProfile
        fields = ('address', 'telephone')

class UserBioForm(forms.ModelForm):
    bio = forms.CharField(max_length=1000, widget=forms.Textarea(
            attrs={'placeholder': 'Tell us a little about yourself...', 'class': 'form-control', 'row': '2'}))

    class Meta:
        model: UserProfile
        fields = ('bio',)


class UserAvatarForm(forms.ModelForm):
    avatar = forms.ImageField()

    class Meta:
        model = UserProfile
        fields = ('avatar',)


class RequestPasswordForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': '*Email...', 'class': 'form-control form-control-lg'}))

    class Meta:
        model = User
        fields = ('email',)


class ForgottenPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*Password...', 'class': 'form-control form-control-lg password'}))

    new_password2 = forms.CharField(max_length=254, required=True,widget=forms.PasswordInput(attrs={'placeholder': '*Re-enter Password...','class': 'form-control form-control-lg password'}))

    class Meta:
        model = User
        fields = ('password1', 'password2')


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*Password...', 'class': 'form-control form-control-lg password'}))

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*Re-enter Password...', 'class': 'form-control form-control-lg password'}))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*Confirm Password...', 'class': 'form-control form-control-lg password'}))

    class Meta:
        model = User
        fields = ('password1', 'password2')


class TwoStepForm(forms.ModelForm):
    two_step_code = forms.CharField(max_length=6, required=True,
        widget=forms.TextInput(attrs={'placeholder': '*Code...'}))

    class Meta:
        model: UserToken
        fields = ('two_step_code',)
