from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
# class LoginForm(forms.Form):
#     username = forms.CharField(widget=forms.TextInput)
#     password = forms.CharField(widget=forms.PasswordInput)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StudentForm(ModelForm):
    class Meta:
        model = Viewer
        fields = [ 'name','phone']

class NewsForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%; height: 50px;'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 100%; height: 250px;'}),
        }