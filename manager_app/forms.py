from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
    UserChangeForm
)

from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from manager_app.models import Publication, Editor, Subject


class PublicationForm(forms.ModelForm):
    executives = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        required=True
    )
    publication_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Publication
        fields = "__all__"


class EditorForm(UserCreationForm):
    experience = forms.IntegerField(
        validators=[MinValueValidator(0),]
    )

    class Meta(UserCreationForm.Meta):
        model = Editor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "experience"
        )


class EditorUpdateForm(UserChangeForm):
    password = None
    experience = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={"min": 0})
    )

    class Meta(UserChangeForm.Meta):
        model = Editor
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "experience"
        ]
        widgets = {
            "username": forms.TextInput(attrs={"readonly": "readonly"}),
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "email": forms.TextInput(attrs={"readonly": "readonly"}),
        }


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ["name",]


class SearchEditorsInPublicationsForm(forms.Form):
    query = forms.CharField(max_length=255, required=False)


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )
    remember_me = forms.BooleanField(required=False, initial=False)
