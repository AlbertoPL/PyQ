from django.conf import settings
from django.conf.urls.defaults import *

from PyQ.pyq.models import Topic

urlpatterns = patterns('',
    url(r'^$', 'PyQ.pyq.views.main_page'),
    url(r'^live/$', 'PyQ.pyq.views.live'),
    url(r'^tag/(.+\+*)+$', 'PyQ.pyq.views.tag'),
    #url(r'^question/(\d+)/$', 'PyQ.pyq.views.post'),
    url(r'^question/$', 'PyQ.pyq.views.ask_question'),
    url(r'^question/submitted/$', 'PyQ.pyq.topic_view.post_topic'),
    url(r'^question/(\d+)/reply/$', 'PyQ.pyq.reply_view.post_reply'),
    url(r'^(?P<topic_type>[^/]+)/(?P<post_id>[^/]+)/comment/$', 'PyQ.pyq.comment_view.comment_handler'),
    url(r'^reply/(?P<reply_id>[^/]+)/vote/$', 'PyQ.pyq.views.vote'),
    url(r'^question/(\d+)/?$', 'PyQ.pyq.topic_view.topic_handler'),
    url(r'^reply/(?P<reply_id>[^/]+)/$', 'PyQ.pyq.reply_view.reply_handler'),
    url(r'^comment/(?P<comment_id>[^/]+)/$', 'PyQ.pyq.comment_view.comment_handler'),	
    url(r'^accounts/login/$', 'PyQ.pyq.views.login_view'),
    url(r'^accounts/logout/$', 'PyQ.pyq.views.logout_view'),
    url(r'^search/$', 'PyQ.pyq.views.search', name="search"),
	url(r'^user_profile/(?P<user_id>[^/]+)/$', 'PyQ.pyq.views.user_profile'),
    
    #These url_conf are hacks to allow django to support static media
    #THEY ARE NOT TO BE USED IN PRODUCTION
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT }),
)
