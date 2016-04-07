from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse

from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required #fancy decorator
from django.contrib.auth.models import User
import json

from .forms import UserForm, PostForm, CommentForm
from .models import UserProfile, Post, Comment

 
# Create your views here.
class Index(View):
    def get(self, request):
        user_form = UserForm()
        post_form = PostForm()
        comment_form = CommentForm()

        context = {
            'user_form': user_form,
            "post_form": post_form,
            "comment_form": comment_form,
            }

        return render(request, "index.html", context)
