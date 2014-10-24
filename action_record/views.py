from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from urlparse import urlparse, parse_qs
from datetime import datetime
from common import init_data
from common import test_redis

def index(request):
    return HttpResponse("action_record Index views")

def data(request):
    test_redis()
    return render_to_response('action_record/data.html', None)

def current_datetime(request):
    now = datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def init_test_data(request):
    url = request.get_full_path()
    parse_url = urlparse(url)
    params = parse_qs(parse_url.query, True)
    user_name = params['user_name'][0]
    user_password = params['password'][0]
    html = None
    html = "<html><title>Init Test Data</title><body>params=%s %s </body></html>" % (user_name, user_password)
    if(user_name is not None and user_name == 'miles.mai' and user_password is not None and user_password == 'xiaomai'):
        result = init_data(None, None)
        if result:
            html = "<html><title>Init Test Data</title><body>Success.</body></html>"
        else:
            html = "<html><title>Init Test Data</title><body>Failed.</body></html>"
    else:
        html = "<html><title>Init Test Data</title><body>user_name or password is error.</body></html>"

    return HttpResponse(html)
