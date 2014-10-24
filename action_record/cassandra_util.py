__author__ = 'miles'

from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
from action_log import action_log

CASS_KEY_SPACE = 'cassandra_zhihu'
CASS_URL = 'localhost:9160'
CASS_COLUMN_FAMILY = 'action_record'

__cass_pool = None

def get_cassandra_column_family(column_family):
    try:
        if __cass_pool is None:
            __cass_pool = ConnectionPool(CASS_KEY_SPACE, [CASS_URL])
        if column_family is None:
            column_family = CASS_COLUMN_FAMILY
        cass_col_family = ColumnFamily(__cass_pool, column_family)
    except Exception, e:
        cass_col_family = None
        print(e)
    return cass_col_family

def get_action_record_by_user_id(user_id):
    try:
        if user_id is None or user_id <= 0:
            result = None
        else:
            col_fam = get_cassandra_column_family(None)
            result = col_fam.get(user_id)
    except Exception, e:
        result = None
        print(e)
    return result

def insert_action_record(data):
    try:
        if data is None or len(data) <= 0:
            result = False
        else:
            col_fam = get_cassandra_column_family(None)
            for item in data:
                if item is action_log and item.is_valid():
                    col_fam.insert(item.user_id, {(str(item.time_line) + str(item.uuid)) : item.action_detail})
            result = True
    except Exception, e:
        result = False
        print(e)
    return result


