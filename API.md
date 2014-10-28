env.py
=====
     环境配置文件
     1. cassandra_setting
         CASS_KEY_SPACE：cassandra数据库的keyspace
         CASS_URL：cassandra数据库的url
         CASS_COLUMN_FAMILY：记录列族名

     2. redis_setting
         REDIS_HOST：Redis数据库Host
         REDIS_PORT：Redis服务端口号
         REDIS_DB：Redis存储的数据库号

     3. file_setting
         TEST_DATA_FILE_PATH：测试数据文件的全路径***/***/**.txt

view.py
======
     与前端交互的主要文件

common.py
=========
     主要业务逻辑处理方法
     1. def create_data_file(user_num, user_record_num)
          创建测试用数据文件
          @params：user_num 用户数，default=10
          @params：user_record_num 用户记录数，default=10
          @return：True
          @error：如果创建文件失败

     2. def init_data_for_test(file)
          读取文件中的记录，调用cassandra_util.insert_action_record()插入Cassandra数据库，初始化数据
          @params：file 数据文件
          @return：True
          @error：如果文件无法打开 or 插入数据库出错

     3. def get_data_from_cass_to_redis(user_id)
          根据user_id，查询Cassandra数据库中的记录，并将该用户全部记录插入Redis中
          @params：user_id 用户ID
          @return：True/False

     4. def get_action_record(user_id, start, end)
          根据user_id查询Redis记录，start&end作为分页参数；
          当找不到记录时，调用get_data_from_cass_to_redis(user_id)方法从Cassandra获取数据；
          若依旧找不到，则返回空List
          @params：user_id 用户ID
          @params：start 分页查询记录开始数
          @params：end 分页查询记录结束数
          @return：List<action_log>


     5. def set_item_anonymity(user_id, item_id)
          根据user_id，设置用户对item_id的主题为匿名状态
          @params：user-id 用户ID
          @params：item_id 主题ID
          @return：True/False

     6. def unset_item_anonymity(user_id, item_id)
          根据user_id，取消用户对item_id主题的匿名状态
          @params：user-id 用户ID
          @params：item_id 主题ID
          @return：True/False

cassandra_util.py
=============
     Cassandra的操作方法
     1. def get_cassandra_column_family(column_family)
          获取Cassandra数据库的column_family
          @params：column_family 列族名
          @return：列族对象 or None
          @error：数据库出错

     2. def insert_action_record(data)
          插入记录到Cassandra的列族中
          @params：data List<action_log> 记录List
          @return：True/False

     3. def get_action_record_by_user_id(user_id)
          根据user_id查询数据库记录
          @params：user_id 用户ID
          @return：数据库记录 Object

redis_util.py
=========
     Redis的操作方法
     1. def get_redis_Redis()
          获取redis链接
          @return：redis.Redis

     2. def insert_action_log(data)
          插入记录到Redis数据库
          @params：data List<action_log>
          @return: True/False

     3. def get_action_record_by_user_id(user_id, start, end)
          获取Redis分页记录
          @params：user_id 用户ID
          @params：start 记录开始位置
          @params：end 记录结束位置
          @return：数据库记录 Object

     4. def set_item_anonymity(user_id, item_id)
          封装设置item_id主题为匿名状态的操作
          @params：user_id 用户ID
          @params：item_id 主题ID
          @return：True/False

     5. def unset_item_anonymity(user_id, item_id)
          封装取消item_id主题匿名状态的操作
          @params：user_id 用户ID
          @params：item_id 主题ID
          @return：True/False

     6. def delete_action_log(user_id, item_id, value_match)
          根据参数删除Redis记录；user_id不为空；
          item_id不为空时，只删除用户对item_id主题的匿名记录；
          value_match===‘user_itemall’时，删除用户对全部主题的匿名记录。
          @params：user_id 用户ID
          @params：item_id 主题ID
          @params：value_match value的匹配规则
          @return：True/False