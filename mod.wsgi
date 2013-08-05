import os, sys
sys.path.append('d:/djangosites')
os.environ['DJANGO_SETTINGS_MODULE'] = 'PyQ.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()