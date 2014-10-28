开发环境
     1. 语言：Python2.7
     2. IDE：Pycharm
     3. 数据库：Redis+Cassandra
     4. 操作系统：max OS 10.9
     5. 其它：Java7u71

系统分析设计
     1. 数据初始化
          a. user_id-action_id-item_id-time_line
          b. 随机产生测试数据
          c. 读取数据初始化数据库
          d. 提供插入新数据的API

     2. 存储结构设计
          a. Cassandra做数据持久化
               user_id作为rowKey，使用复合主键<时间戳:uuid>
               #防止同一时间点同一操作执行多次而相互覆盖记录
               #采用Cassandra还考虑数据分片索引，每次读入redis的数据做到更加合理化。由于涉及匿名问题，分片索引计算没有很好的解决方案，暂时搁置
          b. Redis的sortedSets结构做分页查询
               #zadd zhihu:user_id user_id-action_id-item_id-time_line__uuid time_line
          c. Redis做匿名记录存储
               #zadd zhihu:user_id:item_id user_id-action_id-item_id-time_line__uuid time_line
          4. 用zscan搜索匿名问题，用pipeline做事务，事务中将匿名问题的记录查询出后单独存放，再删除主存储中的相关记录。当匿名取消时，将问题记录再放回主存储中

     3. 系统框架
          项目使用django框架，前端发送ajax请求到后端，经过路由器转发请求相对应的方法，执行数据库相关操作，返回操作结果。
          程序流程
               #见文件目录：static/img/*.img

配置说明
     1. 安装数据库：Redis、Cassandra
     2. 修改配置文件为本地配置：项目路径/action-record/env.py
     3. 在Cassandra中创建key_space及column_family：
          a. key_space：
          b. column_family：
     4. 运行
          a. 使用Pycharm直接导入项目，修改配置后运行。
          b. 控制台命令行进行项目根目录，执行：

测试方法
     a. 如果没有修改默认端口，则在浏览器输入：http://127.0.0.1:8000/action-record/ 可进入主页（本人不会前端，只写了非常简单的页面，用于测试）
     b. 分别点击创建记录、读取记录，用于初始化用户的'最近动态'（测试用，程序写死创建id为1-10的用户，每个用户10条记录。）
     c. 重复步骤2，可生成10个用户的多条记录
     d. 输入user_id、start、end，执行分页查询（JSON格式请在浏览器调试窗口查看，html页面未格式化）
     e. 选择当前记录中的一个item_id，模拟匿名操作（user_id 对 item_id 匿名）
     f. 执行步骤4，可看到匿名效果
     g. 再次模拟取消匿名操作
     h. 执行步骤4，可看到取消匿名的效果
     i. Done.