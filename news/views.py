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

        context = {
            'user_form': user_form,
            "register_form":register_form,
            "post_form": post_form,
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
        posts = Post.objects.all().order_by('-votes')
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

        posts = Post.objects.all().order_by('-votes')
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

        posts = Post.objects.all().order_by('-votes')
        res = [post.to_json() for post in posts]

        if post:
            return JsonResponse({"Message": "Voted Down!", "posts": res})
        else:
            return JsonResponse ({"response":"Invalid information"})


class Delete(View):
    def post(self, request, pk):
        pk = pk
        post = Post.objects.get(pk = pk)
        post.delete()

        posts = Post.objects.all().order_by('-votes')
        res = [post.to_json() for post in posts]

        if res:
            return JsonResponse({"Message": "Deleted", "posts": res})
        else:
            return JsonResponse ({"response":"Invalid information"})


class Edit(View):
    template = "events/index.html"

    def get(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)

        context = {
            "post_id": post.id,
            "edit_form": form.as_p(),}
        return JsonResponse(context)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        if not post:
            return JsonResponse ({"Message":"Invalid information"})
        # this time we get the form with the data
        form = PostForm(data=request.POST, instance=post)

        if form.is_valid():
            event = form.save()
            res = post.to_json()
            return JsonResponse({"Message": "Edited succesfull", "posts": res})
        else:
            return JsonResponse ({"Message":"Invalid information"})


class Make_Comment(View):
    def get(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        comment_form = CommentForm()

        context = {
            "post_id": post.id,
            "comment_form": comment_form.as_p(),}
        return JsonResponse(context)

    def post(self, request, pk):
        if not request.user.is_authenticated():
            # if there is no user logged in they can not submit a comment 
            return HttpResponseForbidden(render (request, "403.html"))

        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            post = Post.objects.get(pk=pk)
            comment = form.save(commit=False)
            # save the user and post to this specific comment, AKA add an FK
            comment.user = user
            comment.post = post
            comment.save()

            res = comment.to_json()
            return JsonResponse({"Message": "Commented", "comments": res})
        else:
            return JsonResponse ({"Message":"Invalid information"})


class Get_Post_Comments(View):
    def post(self, request, pk):
        comments = Comment.objects.filter(post=pk).order_by('-votes')
        res = [comment.to_json() for comment in comments]

        if res:
            return JsonResponse({"comments": res})
        else:
            return JsonResponse ({"response":"You have no Comments"})


class Comment_Up(View):
    def post(self, request, pk):
        pk = pk
        comment = Comment.objects.get(pk = pk)
        comment.votes += 1
        comment.save()

        comments = Comment.objects.filter(pk=pk).order_by('-votes')
        res = [comment.to_json() for comment in comments]

        if res:
            return JsonResponse({"comments": res})
        else:
            return JsonResponse ({"response":"You have no Comments"})


class Comment_Down(View):
    def post(self, request, pk):
        pk = pk
        comment = Comment.objects.get(pk = pk)
        comment.votes -= 1
        comment.save()

        comments = Comment.objects.filter(pk=pk).order_by('-votes')
        res = [comment.to_json() for comment in comments]

        if res:
            return JsonResponse({"comments": res})
        else:
            return JsonResponse ({"response":"You have no Comments"})










# class Edit_Comment(View):
#     template = "edit_comment.html"

#     # here we get the slug id passed in with the url 
#     def get(self, request, comment_slug=None):
#         # get the slug id from the object
#         comment = Comment.objects.get(slug=comment_slug)
#         # get the form and populate it with the value that is already there, AKA what we want to edit
#         comment_form = CommentForm(instance=comment)
#         # send the comment form also
#         context = {
#             "comment": comment,
#             "CommentForm": comment_form}
#         return render(request, self.template, context)


#     def post(self, request, comment_slug=None):
#         # get the slug id from the object
#         comment = Comment.objects.get(slug=comment_slug)  
#         # this time we get the NEW, EDITED content from the form 
#         comment_form = CommentForm(data=request.POST, instance=comment)

#         if comment_form.is_valid():
#             # if the form is valid we save it to the db
#             comment_form.save()
#             return redirect("news:index")
#         else:
#             context = {
#                 "comment": comment,
#                 "CommentForm": comment_form,}
#             # if it is not valid just send it back with the errors attached
#             return render(request, self.template, context)


class Delete_Comment(View):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()

        comments = Comment.objects.all().order_by('-votes')
        res = [comment.to_json() for comment in comments]

        if res:
            return JsonResponse({"Message": "Deleted", "comments": res})
        else:
            return JsonResponse ({"response":"Invalid information"})



            
