from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from PyQ.pyq.models import Post, Topic, TopicForm, Reply, ReplyForm, Comment, Tag, UserProfile
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core import serializers
import urllib

def urldecode(query):
    d = {}
    a = query.split('&')
    for s in a:
        if s.find('='):
            k,v = map(urllib.unquote_plus, s.split('='))
            d[k] = v
    return d

def reply_handler(request, reply_id):
    if request.method == "POST":
        pass
    elif request.method == "PUT":
        return edit_reply(request, reply_id)
    elif request.method == "DELETE":
        return delete_reply(request, reply_id)
    return HttpResponseRedirect("/"+request.method)

@login_required
def delete_reply(request, reply_id):
    reply = Reply.objects.get(id=reply_id)
    if request.user.has_perm("reply.delete_reply") or request.user == reply.topic.parent.user_posted:
        reply.delete()
        try:
            profile = request.user.get_profile()
        except (UserProfile.DoesNotExist):
            profile = UserProfile(user=request.user, num_posts=0, num_comments=0, num_replies=0)
        profile.num_replies = profile.num_replies - 1
        profile.save()
    return HttpResponse(simplejson.dumps({"response": True, "url": "/question/" + str(reply.topic.id) + "/"}), mimetype='application/javascript')

@login_required
def edit_reply(request,reply_id):
    response_dict = {}
    if request.method == "PUT":
        post = Reply.objects.get(id=reply_id)
        if request.user.has_perm("topic.edit_reply"):
            post.parent.text=str(urldecode(request.raw_post_data)["text"])
            post.parent.save()
            response_dict = {"post_text": post.parent.text} 
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

@login_required
def post_reply(request, post_id):
    if request.method == "POST":
        text = request.POST["text"]
        response_dict = {}
        topic = Topic.objects.get(id=post_id)
        response_dict.update({'post_title': topic.title })
        parent = Post(text=text, user_posted=request.user, flag=False,)
        parent.save()
        reply = Reply(parent=parent, vote_count=0, topic=topic,)
        reply.save()
        try:
            profile = request.user.get_profile()
        except (UserProfile.DoesNotExist):
            profile = UserProfile(user=request.user, num_posts=0, num_comments=0, num_replies=0)
        profile.num_replies = profile.num_replies + 1
        profile.save()
        response_dict.update({'post_text': reply.parent.text, 'post_timestamp': str(reply.parent.timestamp),'user': request.user.username, "num_posts":profile.num_posts,"num_replies":profile.num_replies, "num_comments":profile.num_comments,})
        json = simplejson.dumps(response_dict)
        return HttpResponse(json, mimetype='application/javascript')
    else:
        return HttpResponseRedirect("/question/" + str(post_id) + "/")
