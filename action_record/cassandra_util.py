__author__ = 'miles'

from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
import action_log
import env

__cass_pool = None

def get_cassandra_column_family(column_family):
    try:
        global __cass_pool
        if __cass_pool is None:
            __cass_pool = ConnectionPool(env.CASS_KEY_SPACE, [env.CASS_URL])
        if column_family is None:
            column_family = env.CASS_COLUMN_FAMILY
        cass_col_family = ColumnFamily(__cass_pool, column_family)
    except Exception, e:
        cass_col_family = None
        print(e)
    return cass_col_family

def get_action_record_by_user_id(user_id):
    try:
        if user_id is None or user_id <= 0 or len(str(user_id)) <= 0:
            result = None
        else:
            col_fam = get_cassandra_column_family(None)
            result = col_fam.get(str(user_id))
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
                if isinstance(item, action_log.action_log) and item.is_valid():
                    col_fam.insert(str(item.user_id), {(str(item.time_line), str(item.uuid)) : str(item.action_detail)})
            result = True
    except Exception, e:
        result = False
        print(e)
    return result


