from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea, CheckboxInput, PasswordInput
from .models import UserProfile, Post, Comment


# form used to register a user
class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ("first_name", "last_name", "username", "email", "password1", "password2")

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]
        widgets = {
            # this sets the input text area
            "password": PasswordInput(),
        }

# form used to create and edit a post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "link",
            "content",
        ]
        widgets = {
            # this sets the input text area
            "content": Textarea(attrs={"cols": 60, "rows": 10}),
            "link": forms.TextInput(attrs={'placeholder': 'https://www.google.com'})
        }

# form used to create and edit a comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "title",
            "link",
            "content",
        ]
        widgets = {
            "content": Textarea(attrs={"cols": 30, "rows": 5})
        }

