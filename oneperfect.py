
import openai
from flask import Flask, request, jsonify, Response, make_response,stream_with_context
from flask_cors import CORS
import json
import online
import time
import requests


app = Flask(__name__)
CORS(app)


# 构造回复
response_content={
                    "choices": [
                        {
                            "delta": {
                                "content": "oneperfect"
                            }
                        }
                    ]
                }

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

    key = extract_token_from_headers()

    # 调用官方3.5 联网
    if model_name =="gpt-3.5-online":    # 添加自定义模型的名称
        openai.api_key = key.strip()
        def generate():
            print(message)
            messages= message[-1]["content"]
            urls = online.google(messages)
            for index, url in enumerate(urls[:5]):
                res = online.scrape_text(url['link'])
                i_say = "这是第{}条搜索结果。".format(index) + res.strip() + "\n" + "对该搜索结果进行总结，然后回答问题：{}。如果你无法找到问题的答案，则不需要返回总结的结果，仅简单的返回结果即可。".format(messages)
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                                        messages=[
                                                            {"role": "system","content": "请从以下给定的搜索结果中抽取信息，并对搜索结果进行总结，然后回答问题。如果你无法找到问题的答案，则不需要返回总结的结果，仅简单的返回结果即可。"},
                                                            {"role": "user", "content": i_say}
                                                        ],
                                                        temperature=0.9,
                                                        stream=True, top_p=1, frequency_penalty=0,
                                                        presence_penalty=0,
                                                        )
                response_content["choices"][0]["delta"]["content"] = "\n\n\n第{}条搜索结果\n".format(index)
                yield f'data: {json.dumps(response_content)}\n\n'
                for r in response:
                    if 'content' in r.choices[0].delta:
                        yield f'data: {json.dumps(r)}\n\n'
            yield 'data: {"choices": [{"delta": {"content": "[DONE]\n"}}]}\n\n'

        response = Response(stream_with_context(generate()), content_type='text/event-stream')
        return response

    # 调用官方画图
    if model_name == "image":
        openai.api_key = key.strip()
        def generate():
            messages= message[-1]["content"]

            res = openai.Image.create(
                prompt=messages,
                n=1,
                size="256x256"
            )

            reply_content = "这是你的回复，请及时保存，一段时间该图片将被删除\n\n" + "![图像描述]({})".format(res['data'][0]['url'])
            response_content["choices"][0]["delta"]["content"] = reply_content
            yield f'data: {json.dumps(response_content)}\n\n'
            yield 'data: {"choices": [{"delta": {"content": "[DONE]\n"}}]}\n\n'

        response = Response(stream_with_context(generate()), content_type='text/event-stream')
        return response


    # 调用百度文心一言
    if model_name =="wxyy" :

        messages = message[-1]["content"]
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={}".format(key.strip())

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": messages
                }
            ],
            "stream": True
        })
        headers = {
            'Content-Type': 'application/json'
        }


        def generate():
            response = requests.request("POST", url, headers=headers, data=payload, stream=True)
            for R in response.iter_lines():
                if R:
                    rep = R.decode('utf-8')
                    cont = json.loads(rep[6:])["result"]
                    for c in cont:
                        time.sleep(0.05)
                        #print(c, end="", flush=True)
                        response_content["choices"][0]["delta"]["content"] = c
                        yield f'data: {json.dumps(response_content)}\n\n'


            yield 'data: {"choices": [{"delta": {"content": "[DONE]"}}]}\n\n'
        response = Response(stream_with_context(generate()), content_type='text/event-stream')
        return response

    else:
        return "error"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=15413)

