from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from PyQ.pyq.models import Post, Topic, TopicForm, Reply, ReplyForm, Comment, Tag, UserProfile
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def paginate(request, item_list, num_pages=25):
    paginator = Paginator(item_list, num_pages)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)
    
    return items

# Create your views here.
def main_page(request):
    topic_list = Topic.objects.all()
    tags = Tag.objects.all()
    topics = paginate(request, topic_list)
    profile = None
    if isinstance(request.user, User):
        try :
            profile = request.user.get_profile()
        except (UserProfile.DoesNotExist):
            profile = UserProfile(user=request.user, num_posts=0, num_comments=0, num_replies=0)
            profile.save()
    return render_to_response("live.html", {"topics":topics,"tags":tags,"user":request.user,"profile":profile,})

def live(request):
    topic_list = Topic.objects.all()
    tags = Tag.objects.all()
    topics = paginate(request, topic_list)
    try:
        profile = request.user.get_profile()
    except (UserProfile.DoesNotExist):
        profile = UserProfile(user=request.user, num_posts=0, num_comments=0, num_replies=0)
        profile.save()
    return render_to_response("live.html", {"topics":topics,"tags":tags,"user":request.user,"profile":profile,})

def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    try :
        profile = request.user.get_profile()
    except (UserProfile.DoesNotExist):
        profile = UserProfile(user=request.user, num_posts=0, num_comments=0, num_replies=0)
        profile.save()
    return render_to_response("user_profile.html", {"user": user, "profile":profile,})

def tag(request, current_tags):
    
    tag_names = current_tags.split('+')
    #tags = []
    append = None
    
    tags = Tag.objects.filter(name__in=tag_names)
    topic_list = []
    for tag in tags:
        for topic in tag.topics.all():
            if not topic in topic_list:
                topic_list.append(topic) 
        
    for tag in tags:    
        for topic in topic_list[:]:
            if not topic in tag.topics.all():
                topic_list.remove(topic)
    
    tags = []
    for topic in topic_list:
        for tag in topic.tag_set.all():
            if tag.name not in tag_names and tag not in tags:
                tags.append(tag)
                
    if tags.__len__() > 0:
        append = current_tags
    
    topics = paginate(request, topic_list, 2)  
    try:
        profile = request.user.get_profile()
    except (UserProfile.DoesNotExist):
        profile = UserProfile(user=request.user, num_posts=0, num_comments=0, num_replies=0)  
        profile.save()
    return render_to_response("live.html", {"topics":topics,"tags":tags,"append":append, "user":request.user,"profile":profile,}) 

@login_required
def ask_question(request):
    form = TopicForm()
    try:
        profile = request.user.get_profile()
    except (UserProfile.DoesNotExist):
        profile = UserProfile(user=request.user, num_posts=0, num_comments=0, num_replies=0)
        profile.save()
    return render_to_response("askquestion.html", {"form":form, "user":request.user,"profile":profile,}
                               )

def search(request):
    topics = []
    tags = []
    if 'search_input' in request.GET:
        term = request.GET['search_input']
        topic_list = Topic.objects.filter(Q(title__contains=term) or Q(text__contains=term))
        topics = paginate(request, topic_list, 2)
        for topic in topic_list:
            for tag in topic.tag_set.all():
                if tag not in tags:
                    tags.append(tag)
        return render_to_response("live.html", {"topics":topics,"tags":tags,})

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    request_dict = {}
    if user is not None:
        if user.is_active:
            login(request, user)
            request_dict.update({'user': user,})
            json = serializers.serialize("json", User.objects.filter(username=user.username))
        else:
            request_dict.update({'error': "This user's account has been disabled", })
            json = simplejson.dumps(request_dict)
    else:
        request_dict.update({'error': "Invalid username/password", })
        json = simplejson.dumps(request_dict)

    return HttpResponse(json, mimetype='application/javascript')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required 
def vote(request, reply_id):
    if request.method == "POST":
        vote = request.POST["vote"]
        post = Reply.objects.get(id=reply_id)
        response_dict = {}
        if vote == "up" and request.user != None:
            if request.user not in post.vote_ups.all() and request.user not in post.vote_downs.all():
                post.vote_count = post.vote_count + 1
                post.vote_ups.add(request.user)
                response_dict = {'vote': 'upvote'}
            elif request.user in post.vote_ups.all() and request.user not in post.vote_downs.all():
                post.vote_count = post.vote_count - 1
                post.vote_ups.remove(request.user)
                response_dict = {'unvote': 'upvote'}
            elif request.user not in post.vote_ups.all() and request.user in post.vote_downs.all():
                post.vote_count = post.vote_count + 2
                post.vote_downs.remove(request.user)
                post.vote_ups.add(request.user)
                response_dict = {'vote': 'upvote', 'unvote': 'downvote'}
        elif vote == "down" and request.user != None:
            if request.user not in post.vote_downs.all() and request.user not in post.vote_ups.all():
                post.vote_count = post.vote_count - 1
                post.vote_downs.add(request.user)
                response_dict = {'vote': 'downvote'}
            elif request.user in post.vote_downs.all() and request.user not in post.vote_ups.all():
                post.vote_count = post.vote_count + 1
                post.vote_downs.remove(request.user)
                response_dict = {'unvote': 'downvote'}
            elif request.user not in post.vote_downs.all() and request.user in post.vote_ups.all():
                post.vote_count = post.vote_count - 2
                post.vote_ups.remove(request.user)
                post.vote_downs.add(request.user)
                response_dict = {'vote': 'downvote', 'unvote': 'upvote'}
        #response_dict = {'vote_count': post.vote_count}
        post.save()
        json = simplejson.dumps(response_dict)
        #return HttpResponseRedirect("/question/" + str(post_id) + "/")
        return HttpResponse(json, mimetype='application/javascript')
