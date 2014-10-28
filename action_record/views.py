from django.shortcuts import render_to_response
from django.http import HttpResponse
from urlparse import urlparse, parse_qs
import common
import env

def index(request):
    return render_to_response('action_record/index.html', None)

def create_test_data_file(request):
    result = common.create_data_file(None, None)
    if result:
        html = "<p>Success.</p>"
    else:
        html = "<p>Failed.</p>"
    return HttpResponse(html)

def read_test_data_file(request):
    result = common.init_data_for_test(env.TEST_DATA_FILE_PATH)
    if result:
        html = "<p>Success.</p>"
    else:
        html = "<p>Failed.</p>"
    return HttpResponse(html)

def query_user_action_record(request):
    url = request.get_full_path()
    parse_url = urlparse(url)
    params = parse_qs(parse_url.query, True)
    user_id = params['user_id'][0]
    start = params['start'][0]
    end = params['end'][0]
    result = common.get_action_record(user_id, start, end)
    return HttpResponse(result)

def set_item_anonymity(request):
    url = request.get_full_path()
    parse_url = urlparse(url)
    params = parse_qs(parse_url.query, True)
    user_id = params['user_id'][0]
    item_id = params['item_id'][0]
    result = common.set_item_anonymity(user_id, item_id)
    return HttpResponse(result)

def unset_item_anonymity(request):
    url = request.get_full_path()
    parse_url = urlparse(url)
    params = parse_qs(parse_url.query, True)
    user_id = params['user_id'][0]
    item_id = params['item_id'][0]
    result = common.unset_item_anonymity(user_id, item_id)
    return HttpResponse(result)
