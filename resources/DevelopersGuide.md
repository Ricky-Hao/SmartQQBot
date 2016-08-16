Developer's Guide
-----------------

QQBot提供的二次开发接口主要是针对插件，基础框架的贡献请提Issue和PullRequest

## 插件开发

### How Plugin Works
插件本质上是一个Python文件或者Python模块，通过将注册事件监听器到MessageObserver，
在收到消息的时候，调用插件文件内注册好的Callback

### Quick Start

###插件编写教程
sql库是内置的对数据库进行操作的一个接口
其提供了
+   sql.execute(s)      ：用于执行不需要返回值的sql命令。s：字符串
+   sql.fetch_all(s)    ：用于执行需要返回全部结果的sql命令。s：字符串
+   sql.fetch_one(s)    ：用于执行需要返回一条结果的sql命令。s：字符串
+   sql.check_table(table_name)     ：用于检测表 table_name 是否已存在（即插件是否已数据库初始化）。
                                   返回值： True 已初始化，False 未初始化



#utils库
+ import smart_qq_bot.utils as utils
包含了以下几个函数
+ in_plugins(account,account_type,plugin_name)   :用于检测该账号是否在插件列表中
+ is_match(pattern,string)   :正则函数，返回re.match对象
+ get_account_and_type(msg)  :获得对应消息的账号与账号类型，return (account,account_type)
+ check_table(table_name)     ：用于检测表 table_name 是否已存在（即插件是否已数据库初始化）。
                             返回值： True 已初始化，False 未初始化


#logger是向控制台输出消息的对象
+   logger.info(string)     输出Info信息
+   logger.debug(string)    输出Debug信息，仅在Debug模式有效
+   logger.error(string)    输出错误信息



#signals分为三种
+   on_all_message      所有信息都将被送往标记函数
+   on_group_message    只有群消息将被送往标记函数
+   on_private_message  只有私聊消息将被送往标记函数

#如何标记函数
+ @on_all_message(name='plugin_name')
+ def marked_fun(msg,bot)
   其中msg为需要处理的消息，bot为机器人对象



#msg的属性
+   msg.content     消息的文本内容
+   msg.from_uin    消息的发送uin，为int类型

#bot的方法
+   bot.get_group_info(group_code=str(msg.from_uin))    获取群消息msg发送者的群信息
                                                       返回字典类型
                                                       {
                                                           'name':         "群名",
                                                           'id':            12345678,
                                                           'group_code':    87654321
                                                       }
+   bot.uin_to_account(msg.from_uin))                   返回私聊消息msg发送者的QQ号
                                                       返回int型



#插件大体可以分为四部分
一、常量部分
+   定义下文需要用到的各种常量
+   定义HELP常量，以便于生成帮助文件
二、初始化代码部分
+   该部分代码用于判断及初始化插件数据库。
+   初始化插件的加载。
+   刷新数据等等。
三、内部函数部分
+   定义需要用到的内部函数
四、调用函数部分
+   该部分函数将会被 signals 标记，即会有消息被送往

#### 开发内置插件

1. 创建一个文件 `sample_plugin.py`，放置到smart\_qq_plugins文件夹内

```python
# coding: utf-8
from random import randint

from smart_qq_bot.messages import GroupMsg, PrivateMsg
from smart_qq_bot.signals import on_all_message, on_bot_inited
from smart_qq_bot.logger import logger
import smart_qq_bot.utils as utils

plugin_name="SamplePlugin"
HELP={
    1,"Someplugin name",
    2,"!someplugin command"
}

@on_bot_inited("PluginManager")
def manager_init(bot):
    logger.info("Plugin Manager is available now:)")

@on_all_message(name=plugin_name)
def sample_plugin(msg, bot):
    """
    :type bot: smart_qq_bot.bot.QQBot
    :type msg: smart_qq_bot.messages.GroupMsg
    """
    (account,account_type)=utils.get_account_and_type(msg)
    if utils.in_plugins(account,account_type,plugin_name):
        # 发送一条群消息
        msg_id = randint(1, 10000)
        if isinstance(msg, GroupMsg):
            bot.send_group_msg("msg", msg.from_uin, msg_id)
        # 发送一条私聊消息
        elif isinstance(msg, PrivateMsg):
            bot.send_friend_msg("msg", msg.from_uin, msg_id)
```

2. 在plugin.json中，`plugin_on`字段中，填入新插件名字，文件可能是这样
```json
{
  "plugin_packages": [],
  "plugin_on": [
      "Activate",
      "Nickname",
      "sample_plugin"
  ]
}
```

3. 启动机器人，会在console看到插件已经载入

#### 将一个Python包作为插件使用

1. 参考内置插件的开发方式，使用相同的方式写插件，但是作为一个独立的Python包。
唯一要注意的地方是，确保Python在import这个Package的时候，所有的"on_all_message"一类
的信号装饰器必须全部被执行，否则将无法成功注册这个插件。

2. 在plugin.json中的`plugin_packages`, 增加一个字段`your_plugin_package_name`,
增加后的文件可能是这样的（包名必须在PythonPath里，否则无法导入）.
```
{
  "plugin_packages": ['your_plugin_package_name'],
  "plugin_on": [
      "Activate",
      "Nickname"
  ]
}
```

3. 启动机器人，可以在console里看到插件被载入
