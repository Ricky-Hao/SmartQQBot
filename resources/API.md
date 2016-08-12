API Reference
-------------------


## 可用的Signals

```python
from smart_qq_bot.signals import (
    on_all_message,
    on_group_message,
    on_private_message,
)
```

## 数据库结构
+ 插件管理库`plugins`(account,account\_type,plugin\_name)
+ 昵称库`Nickname`(account,account_type,nickname,content,suffix)

## 可用数据库操作函数Sqlite

```python
import smart_qq_bot.sqlite as sql
#执行语句函数，自动提交，return None
sql.execute("SQL")
#取得查询结果第一行，return ('xxx',) or None
sql.fetch_one("SQL")
#取得全部查询结果，return [('aaa',),('bbb',)] or None
sql.fetch_all("SQL")
```

##可用工具函数Utils

```python
import smart_qq_bot.utils as utils
#查询该账号是否启用特定插件，return true or false
utils.in_plugins(account,account_name,plugin_name)
#检查是否存在特定名字的表，return true or false
utils.check_table("table name")
#返回正则表达式结果，return re.match or None
utils.is_match(pattern,string)
#从消息msg中取得账号account以及账号类型account_type，return (account,account_type)
utils.get_account_and_type(msg)
```
