# chatgpt 插件
### 演示地址：https://fayudjhgfahjb.lovebaby.today/
### [poe逆向功能](./readme_poe.md)--包含此版本所有功能，额外增加了一个poe逆向，可以免费使用poe的所有模型。
## 介绍
包含联网功能

包含画图功能

包含文心一言 

包含在线搜索/播放 音乐和视频 --需修改前端代码---国外用户可能会有版权问题

包含PDF 文档翻译/总结   （需要前端支持文档上传）


## 使用说明
### 1. 安装
```
git clone  https://github.com/CatAnd-Dog/chatgptplugin.git
```
```
cd  chatgptplugin
```
```
docker build -t oneperfect .
```
```
docker run  -p 15413:15413  -v /root/chatgptplugin/config.py:/app/config.py  oneperfect
```

### 2. 使用
1、（可选操作）使用宝塔反代，使用nginx反代
创建一个web站点--(例如：a.example.com)，使用反向代理，反向代理地址为：http://127.0.0.1:15413

2、使用aichat，添加baseurl，地址为刚刚自己创建的web站点.(和第一步的web站点对应 http://a.example.com)

如果第一步没有使用反向代理，那么此处的baseurl地址为：http://IP:15413     （IP为服务器的公网IP）

3、直接使用：     新增以下模型，可以实现对应的不同效果

gpt-3.5-online    联网模型--使用官方的key

image    画图模型--使用官方的key

wxyy    文心一言--使用官方的[access_token](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu)

plugins    在线搜索/播放  音乐和视频

gpt-3.5-turbo-16k、gpt-4、gpt-4-32k    PDF 文档翻译/总结

4、apikey
默认填写官方的key，如果需要使用第三方的中转key，需要先修改config文件的baseurl，修改地址为第三方的地址。

5、[配置文件说明](./readme_config.md)

