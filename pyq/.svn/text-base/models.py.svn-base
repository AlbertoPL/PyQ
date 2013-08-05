from django.db import models
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User

maxNameFieldLength = 30
maxTopicFieldLength = 255

class UserProfile(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)

    num_posts = models.IntegerField()
    num_replies = models.IntegerField()
    num_comments = models.IntegerField()
    
class Post(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_posted = models.ForeignKey(User)
    flag = models.BooleanField()
    
'''define subclasses of post'''
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comment_post")
    parent = models.OneToOneField(Post)
    
class Voteable(models.Model):  
    vote_count = models.IntegerField()
    parent = models.OneToOneField(Post)
    vote_ups = models.ManyToManyField(User, related_name='voteup')
    vote_downs = models.ManyToManyField(User, related_name='votedown')
    
'''define subclasses of voteable'''
class Topic(Voteable):
    title = models.CharField(max_length=maxTopicFieldLength)

    class Meta:
        ordering = ['-parent']

class Reply(Voteable):
    topic = models.ForeignKey(Topic)

class Tag(models.Model):
    name = models.CharField(max_length=maxNameFieldLength)
    topics = models.ManyToManyField(Topic)
    count = models.IntegerField()

    class Meta:
        ordering = ['-count', 'name']

'''define forms used for input'''    
class TopicForm(forms.Form):
    title = forms.CharField(max_length=maxTopicFieldLength)
    topic = forms.CharField(widget=forms.Textarea(), label='Question')
    tags = forms.CharField()
   
class ReplyForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), label='Answer')
