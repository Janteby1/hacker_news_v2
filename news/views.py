from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse

from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required #fancy decorator
from django.contrib.auth.models import User
import json

from .forms import UserForm, PostForm, CommentForm, RegisterForm
from .models import UserProfile, Post, Comment

 
# Create your views here.
class Index(View):
    def get(self, request):
        user_form = UserForm()
        register_form = RegisterForm()
        post_form = PostForm()
        comment_form = CommentForm()

        context = {
            'user_form': user_form,
            "register_form":register_form,
            "post_form": post_form,
            "comment_form": comment_form,
            }

        return render(request, "index.html", context)


class Register(View):
    def post(self, request):
        if request.is_ajax():
            data = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            data = json.loads(body)

        user_form = UserForm(data)
        if user_form.is_valid():
            user = user_form.save()
            return JsonResponse({"Message": "Register succesfull", "success": True})
        else:
            return JsonResponse ({"response":"Invalid information"})


class Login(View):
    def post(self, request):
        if request.is_ajax():
            data = request.POST
        else:
            body = request.body.decode()
            if not body: 
                return JsonResponse ({"response":"Missing Body"})
            data = json.loads(body)

        username = data.get('username')
        password = data.get('password')

        if not (username and password):
            return JsonResponse({'Message':'Missing username or password.'})
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user) 
                username = request.user.username
                return JsonResponse({'Message':'Welcome in!', "username":username})
            else:
                return JsonResponse({'Message':'Username is inactive'})
        else:
            return JsonResponse({'Message':'Invalid `username` or `password`.'})


class Logout(View):
    def post(self, request):
        logout(request)
        return JsonResponse ({"Message":"Logout Successful"})


class Create_Post(View):
    def post(self, request):
        if not request.user.is_authenticated():
            # if there is no user logged in they can not submit a post 
            # this redirects them to a 403 html page with an error message
            return JsonResponse({'Message':'Please sign in to submit a post'})

        form = PostForm(data=request.POST)
        if form.is_valid():
            user = request.user
            post = form.save(commit=False)
            post.user = user 
            post.save()

            res = post.to_json()
            return JsonResponse({'Message':'Post submitted!','post': res})
        else:
            return JsonResponse ({"Message":"Invalid information"})


class Get_All(View):
    def post(self, request):
        posts = Post.objects.all()
        res = [post.to_json() for post in posts]
        if res:
            return JsonResponse({"posts": res})
        else:
            return JsonResponse ({"response":"You have no posts"})


class Up(View):
    def post(self, request, pk):
        pk = pk
        post = Post.objects.get(pk = pk)
        post.votes += 1
        post.save()

        posts = Post.objects.all()
        res = [post.to_json() for post in posts]

        if post:
            return JsonResponse({"Message": "Voted Down!", "posts": res})
        else:
            return JsonResponse ({"response":"Invalid information"})


class Down(View):
    def post(self, request, pk):
        pk = pk
        post = Post.objects.get(pk = pk)
        post.votes -= 1
        post.save()

        posts = Post.objects.all()
        res = [post.to_json() for post in posts]

        if post:
            return JsonResponse({"Message": "Voted Down!", "posts": res})
        else:
            return JsonResponse ({"response":"Invalid information"})











