# redis

## 安装
1. windows下安装redis
[下载地址](https://github.com/MSOpenTech/redis/releases)
下载后解压到C盘 进入此目录后 > 打开CMD 切换到redis目录运行 > redis-server.exe redis.windows.conf
此时redis已启动, 打开另一个cms 输入 redis-cli.exe -h 127.0.0.1 -p 6379
2. ubunru 下安装
sudo apt-get update
sudo apt-get install redis-server
启动=> redis-server 
进入redis终端 redis-cli

## 配置
1. 配置文件默认再安装目录下(ubuntu 一般在 etc/redis/ 下) 的redis.conf
在终端模式下 可以使用 CONFIG GET CONFIG_SETTING_NAME 获取配置项的内容, 例如:
```bash
redis 127.0.0.1:6379> CONFIG GET loglevel   #获取登陆配置

1) 'loglevel'
2) 'notice'
```
CONFIG GET *  获取所有配置项
2. CONFIG 配置方法
`CONFIG SET CONFIG_SETTING_NAME NEW_CONFIG_VALUE`
例如:
`CONFIG SET loglevel "notice"`
3. 部分配置项说明
```bash
daemonize no                    #Redis默认不是以守护进程的方式运行，可以通过该配置项修改，使用yes启用守护进程
pidfile /var/run/redis.pid      #当Redis以守护进程方式运行时，Redis默认会把pid写入/var/run/redis.pid文件，可以通过pidfile指定
port 6379                       #指定Redis监听端口，默认端口为6379
bind 127.0.0.1                  #绑定的主机地址
timeout 300                     #客户端闲置多长时间后关闭连接，如果指定为0，表示关闭该功能
loglevel verbose                #指定日志记录级别，Redis总共支持四个级别：debug、verbose、notice、warning，默认为verbose
logfile stdout                  #日志记录方式，默认为标准输出，如果配置Redis为守护进程方式运行，而这里又配置为日志记录方式为标准输出，则日志将会发送给/dev/null
databases 16                    # 设置数据库的数量，默认数据库为0，可以使用SELECT <dbid>命令在连接上指定数据库id
save <seconds> <changes>        #指定在多长时间内，有多少次更新操作，就将数据同步到数据文件，可以多个条件配合
#redis 默认配置中提供了三个条件,看下面:
save 900 1      #900秒内有一个更改
save 300 10     #300秒内有10个更改
save 60 10000   #60秒内有10000个更改

rdbcompression yes              #指定存储至本地数据库时是否压缩数据，默认为yes，Redis采用LZF压缩，如果为了节省CPU时间，可以关闭该选项，但会导致数据库文件变的巨大
dbfilename dump.rdb             #指定本地数据库文件名，默认值为dump.rdb
dir ./                          #指定本地数据库存放目录
masterauth <master-password>    #当master服务设置了密码保护时，slav服务连接master的密码
requirepass foobared            #设置Redis连接密码，如果配置了连接密码，客户端在连接Redis时需要通过AUTH <password>命令提供密码，默认关闭
maxclients 128                  #设置同一时间最大客户端连接数，默认无限制，Redis可以同时打开的客户端连接数为Redis进程可以打开的最大文件描述符数，如果设置 maxclients 0，表示不作限制。当客户端连接数到达限制时，Redis会关闭新的连接并向客户端返回max number of clients reached错误信息
maxmemory <bytes>               #指定Redis最大内存限制，Redis在启动时会把数据加载到内存中，达到最大内存后，Redis会先尝试清除已到期或即将到期的Key，当此方法处理 后，仍然到达最大内存设置，将无法再进行写入操作，但仍然可以进行读取操作。Redis新的vm机制，会把Key存放内存，Value会存放在swap区
appendonly no                   #指定是否在每次更新操作后进行日志记录，Redis在默认情况下是异步的把数据写入磁盘，如果不开启，可能会在断电时导致一段时间内的数据丢失。因为 redis本身同步数据文件是按上面save条件来同步的，所以有的数据会在一段时间内只存在于内存中。默认为no
appendfilename appendonly.aof   #指定更新日志文件名，默认为appendonly.aof
#指定更新日志条件，共有3个可选值： 
no          #表示等操作系统进行数据缓存同步到磁盘（快） 
always      #表示每次更新操作后手动调用fsync()将数据写到磁盘（慢，安全） 
everysec    #表示每秒同步一次（折中，默认值）
appendfsync everysec        #设置日志 每秒同步一次

vm-enabled no                       #指定是否启用虚拟内存机制，默认值为no
vm-swap-file /tmp/redis.swap        #虚拟内存文件路径，默认值为/tmp/redis.swap，不可多个Redis实例共享
vm-max-memory 0                     #所有大于vm-max-memory的数据存入虚拟内存，为0的时候,其实是所有value都存在于磁盘
glueoutputbuf yes                   #设置在向客户端应答时，是否把较小的包合并为一个包发送，默认为开启
hash-max-zipmap-entries 64          #指定在超过一定的数量或者最大的元素超过某一临界值时，采用一种特殊的哈希算法
hash-max-zipmap-value 512

activerehashing yes                 #指定是否激活重置哈希，默认为开
include /path/to/local.conf         #指定包含其它的配置文件，可以在同一主机上多个Redis实例之间使用同一份配置文件，而同时各个实例又拥有自己的特定配置文件
```

## 数据类型
Redis支持五种数据类型：string（字符串），hash（哈希），list（列表），set（集合）及zset(sorted set：有序集合)
### String
string 类型是二进制安全的。意思是 redis 的 string 可以包含任何数据。比如jpg图片或者序列化的对象,string 类型是 Redis 最基本的数据类型，string 类型的值最大能存储 512MB。
1. 字符串命令:
```bash
SET key value       #设置指定 key 的值
GET key             #获取指定 key 的值。
GETRANGE key start end  #返回 key 中字符串值的子字符
GETSET key value        #将给定 key 的值设为 value ，并返回 key 的旧值(old value)。
GETBIT key offset       #对 key 所储存的字符串值，获取指定偏移量上的位(bit)。
MGET key1 [key2..]      #获取所有(一个或多个)给定 key 的值。
SETBIT key offset value #对 key 所储存的字符串值，设置或清除指定偏移量上的位(bit)。
SETEX key seconds value #将值 value 关联到 key ，并将 key 的过期时间设为 seconds (以秒为单位)。
SETNX key value         #只有在 key 不存在时设置 key 的值。
SETRANGE key offset value       #用 value 参数覆写给定 key 所储存的字符串值，从偏移量 offset 开始。
STRLEN key              #返回 key 所储存的字符串值的长度。
MSET key value [key value ...]      #同时设置一个或多个 key-value 对。
MSETNX key value [key value ...]    #同时设置一个或多个 key-value 对，当且仅当所有给定 key 都不存在。
PSETEX key milliseconds value       #这个命令和 SETEX 命令相似，但它以毫秒为单位设置 key 的生存时间，而不是像 SETEX 命令那样，以秒为单位。
INCR key                #将 key 中储存的数字值增一。
INCRBY key increment    #将 key 所储存的值加上给定的增量值（increment） 。
INCRBYFLOAT key increment   #将 key 所储存的值加上给定的浮点增量值（increment） 。
DECR key                #将 key 中储存的数字值减一。
DECRBY key decrement    #key 所储存的值减去给定的减量值（decrement） 。
APPEND key value        #如果 key 已经存在并且是一个字符串， APPEND 命令将指定的 value 追加到该 key 原来值（value）的末尾。
```
### Hash
Redis hash 是一个键值(key=>value)对集合,Redis hash 是一个 string 类型的 field 和 value 的映射表，hash 特别适合用于存储对象。
1. hash操作命令
```bash
HDEL key field1 [field2]    #删除一个或多个哈希表字段
HEXISTS key field           #查看哈希表 key 中，指定的字段是否存在。
HGET key field              #获取存储在哈希表中指定字段的值。
HGETALL key                 #获取在哈希表中指定 key 的所有字段和值
HINCRBY key field increment #为哈希表 key 中的指定字段的整数值加上增量 increment 。
HINCRBYFLOAT key field increment    #为哈希表 key 中的指定字段的浮点数值加上增量 increment 。
KEYS key                    #获取所有哈希表中的字段
HLEN key                    #获取哈希表中字段的数量
HMGET key field1 [field2]   #获取所有给定字段的值
HMSET key field1 value1 [field2 value2 ]        #同时将多个 field-value (域-值)对设置到哈希表 key 中。
HSET key field value        #将哈希表 key 中的字段 field 的值设为 value 。
HSETNX key field value      #只有在字段 field 不存在时，设置哈希表字段的值。
HVALS key                   #获取哈希表中所有值
HSCAN key cursor [MATCH pattern] [COUNT count]      #迭代哈希表中的键值对。
```
### List
Redis 列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素到列表的头部（左边）或者尾部（右边）
1. list 操作命令
```bash
BLPOP key1 [key2 ] timeout      #移出并获取列表的第一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。
BRPOP key1 [key2 ] timeout      #移出并获取列表的最后一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。
BRPOPLPUSH source destination timeout       #从列表中弹出一个值，将弹出的元素插入到另外一个列表中并返回它； 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。
LINDEX key index                #通过索引获取列表中的元素
LINSERT key BEFORE|AFTER pivot value        #在列表的元素前或者后插入元素
LLEN key                        #获取列表长度
LPOP key                        #移出并获取列表的第一个元素
LPUSH key value1 [value2]       #将一个或多个值插入到列表头部
LPUSHX key value                #将一个值插入到已存在的列表头部
LRANGE key start stop           #获取列表指定范围内的元素
LREM key count value            #移除列表元素
LSET key index value            #通过索引设置列表元素的值
LTRIM key start stop            #对一个列表进行修剪(trim)，就是说，让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除。
RPOP key                        #移除列表的最后一个元素，返回值为移除的元素。
RPOPLPUSH source destination    #移除列表的最后一个元素，并将该元素添加到另一个列表并返回
RPUSH key value1 [value2]       #在列表中添加一个或多个值
RPUSHX key value                #为已存在的列表添加值
```
### Set
Redis的Set是string类型的无序集合,集合中最大的成员数为 232 - 1 (4294967295, 每个集合可存储40多亿个成员)
1. set 操作命令
```bash
SADD key member1 [member2]      #向集合添加一个或多个成员
SCARD key                       #获取集合的成员数
SDIFF key1 [key2]               #返回给定所有集合的差集 返回key1 在key2 中没有的元素
SDIFFSTORE destination key1 [key2]      #返回给定所有集合的差集并存储在 destination 中
SINTER key1 [key2]              #返回给定所有集合的交集    返回两个集合都有的元素
SINTERSTORE destination key1 [key2]     #返回给定所有集合的交集并存储在 destination 中
SISMEMBER key member            #判断 member 元素是否是集合 key 的成员
SMEMBERS key                    #返回集合中的所有成员
SMOVE source destination member         #将 member 元素从 source 集合移动到 destination 集合
SPOP key                        #移除并返回集合中的一个随机元素
SRANDMEMBER key [count]         #返回集合中一个或多个随机数
SREM key member1 [member2]      #移除集合中一个或多个成员
SUNION key1 [key2]              #返回所有给定集合的并集
SUNIONSTORE destination key1 [key2]     #所有给定集合的并集存储在 destination 集合中
SSCAN key cursor [MATCH pattern] [COUNT count]  #迭代集合中的元素
```
### Zset( 有序集合 )
Redis zset 和 set 一样也是string类型元素的集合,且不允许重复的成员,不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。
1. zset 操作命令
```bash
ZADD key score1 member1 [score2 member2]    #向有序集合添加一个或多个成员，或者更新已存在成员的分数
ZCARD key                                   #获取有序集合的成员数
ZCOUNT key min max                          #计算在有序集合中指定区间分数的成员数
ZINCRBY key increment member                #有序集合中对指定成员的分数加上增量 increment
ZINTERSTORE destination numkeys key [key ...]   #计算给定的一个或多个有序集的交集并将结果集存储在新的有序集合 key 中
ZLEXCOUNT key min max                       #在有序集合中计算指定字典区间内成员数量
ZRANGE key start stop [WITHSCORES]          #通过索引区间返回有序集合成指定区间内的成员
ZRANGEBYLEX key min max [LIMIT offset count]    #通过字典区间返回有序集合的成员
ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT]  #通过分数返回有序集合指定区间内的成员
ZRANK key member                            #返回有序集合中指定成员的索引
ZREM key member [member ...]                #移除有序集合中的一个或多个成员
ZREMRANGEBYLEX key min max                  #移除有序集合中给定的字典区间的所有成员
ZREMRANGEBYRANK key start stop              #移除有序集合中给定的排名区间的所有成员
ZREMRANGEBYSCORE key min max                #移除有序集合中给定的分数区间的所有成员
ZREVRANGE key start stop [WITHSCORES]       #返回有序集中指定区间内的成员，通过索引，分数从高到底
ZREVRANGEBYSCORE key max min [WITHSCORES]   #返回有序集中指定分数区间内的成员，分数从高到低排序
ZREVRANK key member                         #返回有序集合中指定成员的排名，有序集成员按分数值递减(从大到小)排序
ZSCORE key member                           #返回有序集中，成员的分数值
ZUNIONSTORE destination numkeys key [key ...]   #计算给定的一个或多个有序集的并集，并存储在新的 key 中
ZSCAN key cursor [MATCH pattern] [COUNT count]  #迭代有序集合中的元素（包括元素成员和元素分值）
```

## 命令
1. redis-cli => 启动redis客户端
2. PING  => 检测redis服务是否启动  PONG 为启动
3. redis-cli -h host -p port -a password   => 远程服务上执行命令
4. 有时候会又中文乱码  要在redis-cli 后加 --raw  例如: redis-cli --raw
5. Redis 键相关的基本命令:
```bash
DEL key             #key存在时删除key
DUMP key            #序列化给定key, 并返回被序列化的值
EXISTS key          #检查key是否存在
EXPIRE key seconds  #为给的key设置过期时间, 单位为s
EXPIREAT key timestamp  #为 key 设置过期时间。 不同在于 EXPIREAT 命令接受的时间参数是 UNIX 时间戳
PEXPIRE key milliseconds # 设置 key 的过期时间以毫秒计
PEXPIREAT key milliseconds-timestamp    #设置 key 过期时间的时间戳(unix timestamp) 以毫秒计
KEYS pattern        #查找所有符合给定模式( pattern)的 key 
MOVE key db         #将当前数据库的 key 移动到给定的数据库 db 当中
PERSIST key         #移除 key 的过期时间，key 将持久保持
PTTL key            #以毫秒为单位返回 key 的剩余的过期时间
TTL key             #以秒为单位，返回给定 key 的剩余生存时间(TTL, time to live)
RANDOMKEY           #从当前数据库中随机返回一个 key
RENAME key newkey   #修改 key 的名称
RENAMENX key newkey #仅当 newkey 不存在时，将 key 改名为 newkey
TYPE key            #返回 key 所储存的值的类型
```
## Redis HyperLogLog
Redis HyperLogLog 是用来做基数统计的算法,HyperLogLog 只会根据输入元素来计算基数，而不会储存输入元素本身.
1. hyperloglog 操作命令
```bash
PFADD key element [element ...]             #添加指定元素到 HyperLogLog 中。
PFCOUNT key [key ...]                       #返回给定 HyperLogLog 的基数估算值。
PFMERGE destkey sourcekey [sourcekey ...]   #将多个 HyperLogLog 合并为一个 HyperLogLog
```

## Redis 发布订阅
Redis 发布订阅(pub/sub)是一种消息通信模式：发送者(pub)发送消息，订阅者(sub)接收消息。
1. 操作命令
```bash
PSUBSCRIBE pattern [pattern ...]                #订阅一个或多个符合给定模式的频道。
PUBSUB subcommand [argument [argument ...]]     #查看订阅与发布系统状态。
PUBLISH channel message                         #将信息发送到指定的频道。
PUNSUBSCRIBE [pattern [pattern ...]]            #退订所有给定模式的频道。
SUBSCRIBE channel [channel ...]                 #订阅给定的一个或多个频道的信息。
UNSUBSCRIBE [channel [channel ...]]             #指退订给定的频道。
```

## Redis 事务
事务流程: 开启事务 =>  命令入队  =>  执行事务
1. 事务命令
```bash
MULTI           #开启事务
EXEC            #执行所有事务内得命令
DISCARD         #取消事务 放弃事务内得所有命令
UNWATCH         #取消watch 对所有key得监视
WATCH key       #监视一个或多个key
```
说明: 事务可以理解为一个打包的批量执行脚本，但批量指令并非原子化的操作，中间某条指令的失败不会导致前面已做指令的回滚，也不会造成后续的指令不做

## Redis 脚本
Redis 脚本使用 Lua 解释器来执行脚本。 Redis 2.6 版本通过内嵌支持 Lua 环境。执行脚本的常用命令为 EVAL。
1. 脚本常用命令
```bash
EVAL script numkeys key [key ...] arg [arg ...]         #执行 Lua 脚本。
EVALSHA sha1 numkeys key [key ...] arg [arg ...]        #执行 Lua 脚本。
SCRIPT EXISTS script [script ...]                       #查看指定的脚本是否已经被保存在缓存当中。
SCRIPT FLUSH                                            #从脚本缓存中移除所有脚本。
SCRIPT KILL                                             #杀死当前正在运行的 Lua 脚本。
SCRIPT LOAD script                                      #将脚本 script 添加到脚本缓存中，但并不立即执行这个脚本。
```

## Reids 连接命令
```bash
AUTH password       #验证密码是否正确
ECHO message        #打印字符串
PING                #查看服务是否运行
QUIT                #关闭当前连接
SELECT index        #切换到指定的数据库
```

## redis 服务器
1. 服务器命令
```bash
BGREWRITEAOF                    #异步执行一个 AOF（AppendOnly File） 文件重写操作
BGSAVE                          #在后台异步保存当前数据库的数据到磁盘
CLIENT KILL [ip:port] [ID client-id]    #关闭客户端连接
CLIENT LIST                     #获取连接到服务器的客户端连接列表
CLIENT GETNAME                  #获取连接的名称
CLIENT PAUSE timeout            #在指定时间内终止运行来自客户端的命令
CLIENT SETNAME connection-name  #设置当前连接的名称
CLUSTER SLOTS                   #获取集群节点的映射数组
COMMAND                         #获取 Redis 命令详情数组
COMMAND COUNT                   #获取 Redis 命令总数
COMMAND GETKEYS                 #获取给定命令的所有键
TIME                            #返回当前服务器时间
COMMAND INFO command-name [command-name ...]    #获取指定 Redis 命令描述的数组
CONFIG GET parameter            #获取指定配置参数的值
CONFIG REWRITE                  #对启动 Redis 服务器时所指定的 redis.conf 配置文件进行改写
CONFIG SET parameter value      #修改 redis 配置参数，无需重启
CONFIG RESETSTAT                #重置 INFO 命令中的某些统计数据
DBSIZE                          #返回当前数据库的 key 的数量
DEBUG OBJECT key                #获取 key 的调试信息
DEBUG SEGFAULT                  #让 Redis 服务崩溃
FLUSHALL                        #删除所有数据库的所有key
FLUSHDB                         #删除当前数据库的所有key
INFO [section]                  #获取 Redis 服务器的各种信息和统计数值
LASTSAVE                        #返回最近一次 Redis 成功将数据保存到磁盘上的时间，以 UNIX 时间戳格式表示
MONITOR                         #实时打印出 Redis 服务器接收到的命令，调试用
ROLE                            #返回主从实例所属的角色
SAVE                            #同步保存数据到硬盘
SHUTDOWN [NOSAVE] [SAVE]        #异步保存数据到硬盘，并关闭服务器
SLAVEOF host port               #将当前服务器转变为指定服务器的从属服务器(slave server)
SLOWLOG subcommand [argument]   #管理 redis 的慢日志
SYNC                            #用于复制功能(replication)的内部命令
```

## Redis 数据备份与恢复
1. 备份  
    SAVE 备份数据到redis得安装目录中 默认文件名 dump.rdb
    BGSAVE  在后台执行备份
2. 恢复  只需将备份文件 (dump.rdb) 移动到 redis 安装目录并启动服务即可。获取 redis 目录可以使用 CONFIG 命令
CONFIG GET dir 获取redis安装目录

## 安全
- 密码
```bash
CONFIG get requirepass  #查看是否设置了密码验证
CONFIG set requirepass "passwd" #设置密码为passwd
AUTH passwd     #进入redis终端后验证密码
```
## Redia 性能测试
1. 测试基本命令
`redis-benchmark [option] [option value]`
注意: 此命令实在redis得目录下执行,而不是redis得终端下
2. 测试工具可选参数
```bash
-h	指定服务器主机名	   默认: 127.0.0.1
-p	指定服务器端口	        默认：6379
-s	指定服务器 socket	
-c	指定并发连接数	        默认: 50
-n	指定请求数             默认: 10000
-d	以字节的形式指定 SET/GET 值的数据大小	    默认: 2
-k	1=keep alive 0=reconnect	    默认: 1
-r	SET/GET/INCR 使用随机 key, SADD 使用随机值	
-P	通过管道传输 <numreq> 请求	     默认:    1
-q	强制退出 redis。仅显示 query/sec 值	每秒得请求
--csv	以 CSV 格式输出	
-l	生成循环，永久执行测试	
-t	仅运行以逗号分隔的测试命令列表。	
-I	Idle 模式。仅打开 N 个 idle 连接并等待
```
3. 例
```bash
root@ym:/var/lib/redis# redis-benchmark -h 127.0.0.1 -p 6379 -t set,lpush -n 10000 -q

38461.54 requests per second
LPUSH: 41666.67 requests per second
```

## 客户端连接
1. 查看redis当前最大可连接得clients (可在redis.conf中配置)
`CONFIG GET maxclients` 
2. 在启动服务得时候设置最大连接数
`redis-server --maxclients 100000`
3. 客户端命令
```bash
CLIENT LIST	    #返回连接到 redis 服务的客户端列表
CLIENT SETNAME	#设置当前连接的名称
CLIENT GETNAME	#获取通过 CLIENT SETNAME 命令设置的服务名称
CLIENT PAUSE	#挂起客户端连接，指定挂起的时间以毫秒计
CLIENT KILL	    #关闭客户端连接
```

##