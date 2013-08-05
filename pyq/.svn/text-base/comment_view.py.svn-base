from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from PyQ.pyq.models import Post, Topic, TopicForm, Reply, ReplyForm, Comment, Tag, UserProfile
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core import serializers

def comment_handler(request, **kwargs):
    if request.method == "POST":
        return post_comment(request, kwargs["post_id"], kwargs["topic_type"])
    elif request.method == "PUT":
        return edit_comment(request, kwargs["post_id"])
    elif request.method == "DELETE":
        return delete_comment(request, kwargs["comment_id"])
    return HttpResponseRedirect("/" + request.method)  

@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user.has_perm("comment.delete_comment") or request.user == comment.parent.user_posted:
        comment.delete()
        try:
            profile = request.user.get_profile()
        except (UserProfile.DoesNotExist):
            profile = UserProfile(user=request.user, num_posts=0, num_comments=0, num_replies=0)
        profile.num_comments = profile.num_comments - 1
        profile.save()
    return HttpResponse(simplejson.dumps({'response': True, 'comment_id': comment.id}), mimetype='application/javascript')

@login_required
def edit_comment(request, post_id, comment_id):
    if request.method == "POST":
        post = Reply.objects.get(id=comment_id)
        if request.user.has_perm("topic.edit_comment"):
            post.parent.text=request.POST["text"]
            post.save()
    return HttpResponseRedirect("/question/" + str(post_id) + "/")

@login_required
def post_comment(request, post_id, topic_type):
    text = request.POST["text"]
    response_dict = {}
    if topic_type == "question":
        post=Topic.objects.get(id=post_id)
    else:
        post=Reply.objects.get(id=post_id)
    parent = Post(text=text, user_posted=request.user, flag=False,)
    parent.save()
    comment = Comment(post=post.parent, parent=parent,)
    comment.save()
    try:
        profile = request.user.get_profile()
    except (UserProfile.DoesNotExist):
        profile = UserProfile(user=request.user, num_posts=0, num_comments=0, num_replies=0)
    profile.num_comments = profile.num_comments + 1
    profile.save()
    response_dict.update({'post_text': comment.parent.text, 'comment_id': comment.id, 'post_timestamp': str(comment.parent.timestamp),'user': request.user.username, "num_posts":profile.num_posts,"num_replies":profile.num_replies, "num_comments":profile.num_comments,})
    json = simplejson.dumps(response_dict)
    return HttpResponse(json, mimetype='application/javascript')
