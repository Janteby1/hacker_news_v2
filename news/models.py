from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone #make sure to set the timezone 

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	'''
	we can add aditional attributes but Included in the django user model are these attributes:
	Username, Password, Email address, firstname, lastname
	'''

class Post(models.Model):
    title = models.CharField(max_length=40)
    link = models.URLField(max_length=120, null = True, default = None)
    content = models.CharField(max_length=4000)

    slug = models.SlugField(max_length=40)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    show = models.BooleanField(default=True)
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(User, default = 1) # adds a FK

    # this is a custom save method
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.updated_at = timezone.now()
        if not self.id:
            self.created_at = timezone.now()
        super(Post, self).save(*args, **kwargs)

    # this create a dictionary from an object to use with ajax
    def to_json(self):
        return {
            "title": self.title,
            "link": self.link,
            "content": self.content,
            "slug": self.slug,
            "created_at": self.created_at, 
            "show": self.show,
            "votes": self.votes,
            "user": self.user,
        }


class Comment(models.Model):
    title = models.CharField(max_length=40, default = None)
    link = models.URLField(max_length=120, null = True, default = None)
    content = models.CharField(max_length=4000)
    
    slug = models.SlugField(max_length=40)
    created_at = models.DateTimeField(editable=False)
    
    show = models.BooleanField(default=True)
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(User) # adds a FK for user 
    post = models.ForeignKey(Post) # adds a FK for the post it belongs to

    # this is a custom save method
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.id:
            self.created_at = timezone.now()
        super(Comment, self).save(*args, **kwargs)

    # this create a dictionary from an object to use with ajax
    def to_json(self):
        return {
            "title": self.title,
            "link": self.link,
            "content": self.content,
            "slug": self.slug,
            "created_at": self.created_at, 
            "show": self.show,
            "votes": self.votes,
            "user": self.user.id,
            "post": self.post.id,
        }

