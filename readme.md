# chatgpt 插件
## 介绍
包含联网功能

包含画图功能


## 使用说明
### 1. 安装
```
git clone  
```
```
cd  chatgptplugin
```
```
docker build -t oneperfect .
```
```
docer run  -p 15413:15413  oneperfect
```

### 2. 使用
1、使用宝塔反代
创建一个web站点，使用反向代理，反向代理地址为：http://127.0.0.1:15413

2、使用nginx反代
使用aichat，添加baseurl，地址为刚刚自己创建的web站点

3、直接使用
创建模型：
gpt-3.5-online    联网模型
image      画图模型

4、apikey
填写官方的key，推荐使用120刀的key