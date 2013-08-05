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

def http_handler(request, post_id):
    if request.method == "POST":
        pass
    elif request.method == "GET":
        return post_live(request, post_id)
    elif request.method == "PUT":
        return edit_live(request, post_id)
    elif request.method == "DELETE":
        return delete_live(request, post_id)
    #return HttpResponseRedirect("/" + request.method)

def post(request, post_id):
    try: 
        topic=Topic.objects.get(id=post_id)
    except Topic.DoesNotExist:
        return render_to_response("topic_list.html",)
    title = topic.title
    text = topic.parent.text
    timestamp = topic.parent.timestamp
    tags = topic.tag_set.all()
    replies = topic.reply_set.all()
    comments = topic.parent.comment_post.all()
    form = ReplyForm()
    comment_form = ReplyForm()
    try:
        profile = request.user.get_profile()
    except (UserProfile.DoesNotExist):
        profile = UserProfile(user=request.user, num_posts=0, num_comments=0, num_replies=0)
        profile.save()
    return render_to_response("question.html", {"post_title":title, "post_text":text, 
                                "post_timestamp":timestamp, "post_id":post_id, 
                                "post_replies":replies, "post_comments":comments, "form":form, "comment_form":comment_form, "tags":tags, "user":request.user, "javascript":"main.js","style":"question.css","profile":profile,}
                                )

@login_required
def delete_live(request, post_id):
    request_dict = {}
    if request.user.has_perm("livequestion.delete_live"):
        post = Topic.objects.get(id=post_id)
        parent = post.parent
        for tag in post.tag_set.all():
            tag.count = tag.count - 1;
            tag.save()
            if tag.count == 0:
                tag.delete()
        post.delete()
        parent.delete()
        request_dict["response"] = True
        request_dict["url"] = "/"
        try:
            profile = request.user.get_profile()
        except (UserProfile.DoesNotExist):
            profile = UserProfile(user=request.user, num_posts=0, num_comments=0, num_replies=0)
        profile.num_posts = profile.num_posts - 1
        profile.save()
    else:
        request_dict["response"] = "No such topic to delete!"
        request_dict["url"] = "/question/" + str(post_id) + "/"
    return HttpResponse(simplejson.dumps(request_dict), mimetype='application/javascript')
    #return HttpResponseRedirect("/question/" + str(post_id) + "/")
    
@login_required
def edit_live(request, post_id):
    response_dict = {}
    if request.method == "PUT":
        post = Topic.objects.get(id=post_id)
        if request.user.has_perm("livequestion.edit_live"):
            #post.parent.text=urldecode(request.raw_post_data)
            post.parent.text=str(urldecode(request.raw_post_data)["post_text"])
            post.parent.save()
            response_dict = {"post_text": post.parent.text}
    #return HttpResponseRedirect("/question/" + str(post_id) + "/")
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

@login_required    
def post_live(request):
     if request.method == "POST":
        title = request.POST["post_title"]
        text = request.POST["post_body"]
        parent = Post(text=text, user_posted=request.user, flag=False, )
        parent.save()
        topic = LiveQuestion(parent=parent, vote_count=0, title=title,)
        topic.save()
        tagStrings = request.POST["post_tags"].__str__().lower()
        tagsStrings = tagStrings.split()
        for tagString in tagsStrings:
            try:
                tag = Tag.objects.get(name=tagString)
            except:
                tag = Tag(name=tagString,count=0)
            tag.count = tag.count + 1
            tag.save()
            tag.topics.add(topic)
            tag.save()
        profile = request.user.get_profile()
        profile.num_posts = profile.num_posts + 1
        profile.save()
        return HttpResponseRedirect("/question/" + str(topic.id) + "/")