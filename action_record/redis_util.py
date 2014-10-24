__author__ = 'miles'

from redis import ConnectionPool
from redis import Redis
from action_log import action_log

REDIS_HOST = 'localhost'
REDIS_POST = 6379
REDIS_DB = 0

__redis_pool = None
__redis_Redis = None

def get_redis_Redis():
    try:
        if __redis_pool is None:
            __redis_pool = ConnectionPool(REDIS_HOST, REDIS_POST, REDIS_DB)
        if __redis_Redis is None:
            __redis_Redis = Redis(connection_pool=__redis_pool)
    except Exception, e:
        __redis_pool = None
        __redis_Redis = None
        print(e)
    return __redis_Redis

def get_action_record_by_user_id(user_id, start, end):
    try:
        if user_id is None or user_id <= 0 or start is None or start < 0 or end is None or end < start:
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
        if user_id is None or user_id <= 0 or item_id is None or item_id <= 0:
            result = False
        else:
            r = get_redis_Redis()
            items = []
            cursor = -1
            while cursor <> 0:
                if cursor == -1:
                    cursor = 0
                item = r.zscan('zhihu:'+str(user_id), cursor, match='*-'+str(item_id)+'-*')
                items.append(item[0][1])
                cursor = item[0][0]

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
        if user_id is None or user_id <= 0 or item_id is None or item_id <= 0:
            result = False
        else:
            r = get_redis_Redis()
            items = []
            cursor = -1
            while cursor <> 0:
                if cursor == -1:
                    cursor = 0
                item = r.zscan('zhihu:'+str(user_id)+':'+str(item_id), cursor)
                items.append(item[0][1])
                cursor = item[0][0]

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
                if item is action_log and item.is_valid():
                    pipe.zadd('zhihu:'+str(item.user_id), item.action_detail, item.time_line)
            pipe.execute()
            result = True
    except Exception, e:
        result = False
        print(e)
    return result