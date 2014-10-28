__author__ = 'miles'

from redis import ConnectionPool
from redis import Redis
import action_log
import env

__redis_pool = None
__redis_Redis = None

def get_redis_Redis():
    try:
        global __redis_pool, __redis_Redis
        if __redis_pool is None:
            __redis_pool = ConnectionPool(host=env.REDIS_HOST, port=env.REDIS_PORT, db=env.REDIS_DB)
        if __redis_Redis is None:
            __redis_Redis = Redis(connection_pool=__redis_pool)
    except Exception, e:
        __redis_pool = None
        __redis_Redis = None
        print(e)
    return __redis_Redis

def get_action_record_by_user_id(user_id, start, end):
    try:
        if user_id is None or user_id <= 0 or len(str(user_id)) <= 0 or start is None or start < 0 or end is None or end < start:
            result = None
        else:
            r = get_redis_Redis()
            result = r.zrevrange('zhihu:'+str(user_id), start=start, end=end)
    except Exception, e:
        result = None
        print(e)
    return result

def set_item_anonymity(user_id, item_id):
    try:
        if user_id is None or user_id <= 0 or len(str(user_id)) <= 0 or item_id is None or item_id <= 0 or len(str(item_id)) <= 0:
            result = False
        else:
            r = get_redis_Redis()
            items = []
            cursor = -1
            while cursor <> 0:
                if cursor == -1:
                    cursor = 0
                item = r.zscan('zhihu:'+str(user_id), cursor, match='*-'+str(item_id)+'-*__*')
                for record in item[1]:
                    items.append(record)
                cursor = item[0]

            pipe = r.pipeline()
            for item in items:
                pipe.zadd('zhihu:'+str(user_id)+':'+str(item_id), item[0], item[1])
                pipe.zrem('zhihu:'+str(user_id), item[0])
            pipe.execute()
            result = True
    except Exception, e:
        result = False
        print(e)
    return result

def unset_item_anonymity(user_id, item_id):
    try:
        if user_id is None or user_id <= 0 or len(str(user_id)) <= 0 or item_id is None or item_id <= 0 or len(str(item_id)) <= 0:
            result = False
        else:
            r = get_redis_Redis()
            items = []
            cursor = -1
            while cursor <> 0:
                if cursor == -1:
                    cursor = 0
                item = r.zscan('zhihu:'+str(user_id)+':'+str(item_id), cursor, match='*-'+str(item_id)+'-*__*')
                for record in item[1]:
                    items.append(record)
                cursor = item[0]

            pipe = r.pipeline()
            for item in items:
                pipe.zadd('zhihu:'+str(user_id), item[0], item[1])
                pipe.zrem('zhihu:'+str(user_id)+':'+str(item_id), item[0])
            pipe.execute()
            result = True
    except Exception, e:
        result = False
        print(e)
    return result

def insert_action_log(data):
    try:
        if data is None or len(data) <= 0:
            result = False
        else:
            r = get_redis_Redis()
            pipe = r.pipeline()
            for item in data:
                if isinstance(item, action_log.action_log) and item.is_valid():
                    pipe.zadd('zhihu:'+str(item.user_id), '__'.join([str(item.action_detail),str(item.uuid)]), float(str(item.time_line)))
            pipe.execute()
            result = True
    except Exception, e:
        result = False
        print(e)
    return result

def delete_action_log(user_id, item_id, value_match):
    if user_id is None or len(str(user_id)) <= 0:
        return False
    if item_id is None or len(str(item_id)) <= 0:
        key = ':'.join(['zhihu', str(user_id)])
    else:
        key = ':'.join(['zhihu', str(user_id), str(item_id)])

    if value_match is not None and str(value_match) == 'user_itemall':
        key = ':'.join(['zhihu', str(user_id), '*'])
        value_match = None
    try:
        r = get_redis_Redis()
        items = []
        keys = r.keys(key)
        for key in keys:
            cursor = -1
            while cursor <> 0:
                if cursor == -1:
                    cursor = 0
                item = r.zscan(key, cursor, match=value_match)
                for record in item[1]:
                    items.append(record)
                cursor = item[0]
        pipe = r.pipeline()
        for item in items:
            pipe.zrem(key, item[0])
        pipe.execute()
        result = True
    except Exception, e:
        print e
        result = False
    return result