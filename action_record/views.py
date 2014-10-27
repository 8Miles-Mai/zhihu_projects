from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from urlparse import urlparse, parse_qs
from datetime import datetime
import common

def index(request):
    return render_to_response('action_record/index.html', None)

def create_test_data_file(request):
    url = request.get_full_path()
    parse_url = urlparse(url)
    params = parse_qs(parse_url.query, True)
    user_name = params['user_name'][0]
    user_password = params['password'][0]
    result = common.create_data_file(None, None)
    if(user_name is not None and user_name == 'miles.mai' and user_password is not None and user_password == 'xiaomai'):
        if result:
            html = "<html><title>Init Test Data</title><body>Success.</body></html>"
        else:
            html = "<html><title>Init Test Data</title><body>Failed.</body></html>"
    else:
        html = "<html><title>Init Test Data</title><body>user_name or password is error.</body></html>"
    return HttpResponse(html)

def read_test_data_file(request):
    result = common.init_data_for_test('/Users/miles/PycharmProjects/zhihu_projects/action_record/test_data.txt')
    if result:
        html = "<html><title>Init Test Data</title><body>Success.</body></html>"
    else:
        html = "<html><title>Init Test Data</title><body>Failed.</body></html>"
    return HttpResponse(html)

def query_user_action_record(request):
    url = request.get_full_path()
    parse_url = urlparse(url)
    params = parse_qs(parse_url.query, True)
    user_id = params['user_id'][0]
    start = params['start'][0]
    end = params['end'][0]
    common.get_action_record(user_id, start, end)

def set_item_anonymity(request):
    url = request.get_full_path()
    parse_url = urlparse(url)
    params = parse_qs(parse_url.query, True)
    user_id = params['user_id'][0]
    item_id = params['item_id'][0]
    common.set_item_anonymity(user_id, item_id)

def unset_item_anonymity(request):
    url = request.get_full_path()
    parse_url = urlparse(url)
    params = parse_qs(parse_url.query, True)
    user_id = params['user_id'][0]
    item_id = params['item_id'][0]
    common.unset_item_anonymity(user_id, item_id)

def data(request):
    # init_data_for_test('/Users/miles/PycharmProjects/zhihu_projects/action_record/test_data.txt')
    # record = cassandra_util.get_action_record_by_user_id('10')
    # result = json.dumps(str(record))
    # get_data_from_cass_to_redis('11')
    # set_item_anonymity(11, 24)
    # unset_item_anonymity(11, 24)
    # result = get_action_record_by_user_id(11, 0, 10)
    # print(result)
    return render_to_response('action_record/data.html', None)
    # return HttpResponse(result)

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
    result = create_data_file(None, None)
    html = "<html><title>Init Test Data</title><body>params=%s %s </body></html>" % (user_name, user_password)
    if(user_name is not None and user_name == 'miles.mai' and user_password is not None and user_password == 'xiaomai'):
        if result:
            html = "<html><title>Init Test Data</title><body>Success.</body></html>"
        else:
            html = "<html><title>Init Test Data</title><body>Failed.</body></html>"
    else:
        html = "<html><title>Init Test Data</title><body>user_name or password is error.</body></html>"

    return HttpResponse(html)
