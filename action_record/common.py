__author__ = 'miles'

import time
from random import randint
from files import write_file
from files import  read_file
from action_log import action_log
import cassandra_util
import redis_util
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def create_data_file(user_num, user_record_num):
    if user_num is None or user_num <= 0:
        user_num = 20
    if user_record_num is None or user_record_num <= 0:
        user_record_num = 10
    data = []
    for user_id in range(10, user_num):
        for index in range(0, user_record_num):
            item = []
            action_id = randint(1, 7)
            item_id = randint(1, 100)
            time_line_id = str(time.time())[:-3]
            item.append(str(user_id))
            item.append(str(action_id))
            item.append(str(item_id))
            item.append(str(time_line_id))
            record = '-'.join(item) + '\n'
            data.append(record)

    write_file('/Users/miles/PycharmProjects/zhihu_projects/action_record/test_data.txt', data)
    return True

def init_data_for_test(file):
    if file is None:
        return False
    data = read_file(file)
    record_list = []
    for line in data:
        detail = str(line).split('-')
        if len(detail) == 4:
            record = action_log(str(detail[0]), str(detail[1])+'-'+str(detail[2]), detail[3], None)
            record_list.append(record)

    cassandra_util.insert_action_record(record_list)
    return True

def get_data_from_cass_to_redis(user_id):
    result = False
    if user_id is None or user_id <= 0 or len(str(user_id)) <= 0:
            result = False
    else:
        record_list = cassandra_util.get_action_record_by_user_id(str(user_id))
        data = []
        for key in record_list:
            time_line = key[0]
            action_uuid = key[1]
            action_detail = record_list[key]
            record = action_log(str(user_id), str(action_detail), str(time_line), action_uuid)
            data.append(record)

        if data is not None and len(data) > 0:
            print data
            result = redis_util.insert_action_log(data)

    return result

def test_test():
    print os.path.join(BASE_DIR,  'templates/action_record/js/')

def get_action_record(user_id, start, end):
    record = None
    if user_id is None or user_id <= 0 or len(str(user_id)) <= 0 or start is None or start < 0 or end is None or end < start:
        result = None
    else:
        record = redis_util.get_action_record_by_user_id(user_id, start, end)
    if record is None:
        get_data_from_cass_to_redis(str(user_id))
        record = redis_util.get_action_record_by_user_id(user_id, start, end)

    result = record
    for item in record:
        print item
    return result

def set_item_anonymity(user_id, item_id):
    if user_id is None or user_id <= 0 or len(str(user_id)) <= 0 or item_id is None or item_id <= 0 or len(str(item_id)) <= 0:
        result = False
    else:
        result = redis_util.set_item_anonymity(str(user_id), str(item_id))
    return result

def unset_item_anonymity(user_id, item_id):
    if user_id is None or user_id <= 0 or len(str(user_id)) <= 0 or item_id is None or item_id <= 0 or len(str(item_id)) <= 0:
        result = False
    else:
        result = redis_util.unset_item_anonymity(str(user_id), str(item_id))
    return result