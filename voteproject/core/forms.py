from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Poll, Choice

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class PollForm(forms.ModelForm):
    voting_deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="Set deadline for this poll"
    )

    class Meta:
        model = Poll
        fields = ['title', 'description', 'voting_deadline']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
