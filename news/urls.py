from django.conf.urls import include, url
from django.contrib import admin
from news import views #gets all our view functions

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),

    url(r'^register$', views.Register.as_view(), name='register'),
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^logout$', views.Logout.as_view(), name='logout'),

    url(r'^create$', views.Create_Post.as_view(), name="create"),
    url(r'^(?P<pk>[\d]+)/edit$', views.Edit.as_view(), name='edit'),
    url(r'^(?P<pk>[\d]+)/delete$', views.Delete.as_view(), name='delete'),

    url(r'^all$', views.Get_All.as_view(), name="all"),
    url(r'^(?P<pk>[\d]+)/up$', views.Up.as_view(), name='up'),
    url(r'^(?P<pk>[\d]+)/down$', views.Down.as_view(), name='down'),

    # # when we create a comment we send the post id to create an FK 
    url(r'^(?P<pk>[\d]+)/comment$', views.Make_Comment.as_view(), name='comment'),
    url(r'^(?P<pk>[\d]+)/getcomments$', views.Get_Post_Comments.as_view(), name='getcomments'),
    url(r'^(?P<pk>[\d]+)/upcomment$', views.Comment_Up.as_view(), name='upcomment'),
    url(r'^(?P<pk>[\d]+)/downcomment$', views.Comment_Down.as_view(), name='downcomment'),

    # url(r'^edit_comment/(?P<comment_slug>[A-Za-z0-9\-\_]+)$', views.Edit_Comment.as_view(), name='edit_comment'),
    url(r'^(?P<pk>[\d]+)/deletecomment$', views.Delete_Comment.as_view(), name='deletecomment'),
]

