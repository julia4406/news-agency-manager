from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    UsernameField,
    PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from manager_app.models import Publication


class PublicationForm(forms.ModelForm):
    executives = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 120}),
        required=True
    )
    publication_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Publication
        fields = "__all__"



#
# class RegistrationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email',)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control',
#             })
#
#
# class LoginForm(AuthenticationForm):
#     username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control"}))
#     password = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={"autocomplete": "current-password", "class": "form-control"}),
#     )
#
#
# class UserPasswordResetForm(PasswordResetForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={
#         'class': 'form-control'
#     }))
#
#
# class UserSetPasswordForm(SetPasswordForm):
#     new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
#         'class': 'form-control'
#     }), label="New Password")
#     new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
#         'class': 'form-control'
#     }), label="Confirm New Password")
#
#
# class UserPasswordChangeForm(PasswordChangeForm):
#     old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
#         'class': 'form-control'
#     }), label='Old Password')
#     new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
#         'class': 'form-control'
#     }), label="New Password")
#     new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
#         'class': 'form-control'
#     }), label="Confirm New Password")