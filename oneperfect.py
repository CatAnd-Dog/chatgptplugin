
# pip install pipreqs  -i  https://pypi.mirrors.ustc.edu.cn/simple/
# pipreqs ./ --encoding=utf8 --force

from flask import Flask, request, jsonify, Response, make_response,stream_with_context
from flask_cors import CORS
import config
from model import generate_online,generate_dalle,generate_baidu,generate_plugin


app = Flask(__name__)
CORS(app)

# 全局变量
oneperfect=config.oneperfect


# 从请求头中提取token
def extract_token_from_headers():
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]  # 去掉 "Bearer " 前缀
    return token

@app.route('/v1/chat/completions', methods=['POST'])
def send_message():

    data=request.json
    model_name=data["model"]
    message=data["messages"]

    key = extract_token_from_headers().strip()

    # 调用官方3.5 联网
    if model_name =="gpt-3.5-online" and oneperfect["gpt-online"]:    # 添加自定义模型的名称

        response = Response(stream_with_context(generate_online(key,message)), content_type='text/event-stream')
        return response

    # 调用官方画图
    if model_name == "image" and oneperfect["gpt-image"]:

        response = Response(stream_with_context(generate_dalle(key,message)), content_type='text/event-stream')
        return response

    # 调用百度文心一言
    if model_name =="wxyy" and oneperfect["baidu-wxyy"]:

        response = Response(stream_with_context(generate_baidu(key,message)), content_type='text/event-stream')
        return response

    if model_name =="plugin" and oneperfect["gpt-plugins"]:
        response = Response(stream_with_context(generate_plugin(key, message)), content_type='text/event-stream')
        return response
    else:
        return "模型不存在或者模型已禁用"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=15413)

