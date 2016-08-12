SmartQQBot
=========
##简介
该版本的SmartQQBot可以在Python3环境下稳定运行。
同时，该版本使用数据库来管理插件的启用与否。
可以针对每个不同的QQ群以及QQ号做到数据隔离和单独开启关闭插件。
本版本只能使用QRcode登陆，并且要手动打开QRcode文件。

+ 使用文档见[User Guide](resources/UserGuide.md)
+ 二次开发[Developers Guide](resources/DevelopersGuide.md)
+ 贡献文档[Contribution Guide](resources/ContributionGuide.md)
+ API 文档[API Reference](resources/API.md)
+ 常见问题[FAQ](resources/FAQ.md)

## 依赖
+ `PIL`

## 快速开始
+ 安装Python 3.x
+ 安装依赖（`pip install PIL`）
+ 命令行运行 `python run.py`
+ 等待弹出二维码进行扫描登陆, 或手动打开脚本所在目录的v.jpg进行扫描。
+ 控制台不在输出登录确认的log的时候就登录成功了
+ 首次登陆过后, 以后的登陆会尝试使用保存的cookie进行自动登录（失败后会一直loop）
+ 配置插件之后, 才能使用QQBot的调教功能（参见下方插件配置）

## 特性

+ 二维码登录
+ 插件支持, 支持原生Python Package, 支持插件热 启用/关闭
+ 群消息, 私聊消息, 通知消息接收和发送

### 基础功能
注: 插件默认只启用了Activate、Nickname插件, 如需其他功能请自行开启

+ 插件管理功能(Activate), 使用`!召唤 昵称`功能来在QQ群以及QQ号内启用相应昵称名字的机器人
+ 昵称唤出功能(Nickname), 可以设定特定昵称来将机器人唤出以及改名
+ 天气查询功能(Weather), 使用`天气 城市`语句, 查询对应城市的天气消息
+ 喵喵喵功能(Meow), 在接收到以“喵”开头，并且重复1乃至更多次“喵”的语句时，发送“喵”*随机个数
+ 网易云音乐查询功能(NetEaseMusic), 使用`音乐 歌曲名`来从网易云查询相应名字的歌曲，选前三个返回歌曲链接

### 内置插件
+ 插件管理器
+ 昵称唤出插件
+ 网易云音乐查询插件
+ 图灵机器人（需要安装requests库）
+ Bing翻译插件
+ 天气查询插件

## 插件配置
### 如何载入插件

1. 将插件放置到smart\_qq_\plugins目录下
2. 复制plugin.json.example为plugin.json
3. 修改启用的插件列表plugin_on

注: 插件名称为你的PythonPackage或者插件文件的名字

## 已知问题
+ 由于WebQQ协议的限制, 机器人回复消息有可能会被屏蔽, 暂时还没有较好的解决方案。
+ <s>加载多个插件后, 可以接受消息, 但无法正确发送(resolved)</s>

## RoadMap

+ 支持每个插件的单独配置文件

## Contributors
+ [Yinzo](https://github.com/Yinzo)
+ [Cheng Gu](https://github.com/gucheen)
+ [winkidney](https://github.com/winkidney)
+ [eastpiger](https://github.com/eastpiger)

