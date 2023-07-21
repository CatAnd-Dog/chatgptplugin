from func  import online
import openai
import json
import config
import requests
import time



# 全局变量
openai.api_base= config.baseurl+"v1"

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


def generate_openai(message):
    content=config.content_online_keyword
    content[-1]["content"]=message
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                            messages=content,
                                            temperature=0.2,
                                            top_p=0.8, frequency_penalty=0,
                                            presence_penalty=0,
                                            )
    return response["choices"][0]["message"]["content"]

# 联网插件
def generate_online(key,message):

    openai.api_key = key
    messages=generate_openai(message[-1]["content"]) # 获取最后一条消息,并进行关键词提取
    print(messages)
    content=config.content_online_reply
    urls = online.google(messages)
    for index, url in enumerate(urls[:5]):
        res = online.scrape_text(url['link'])
        i_say = "这是第{}条搜索结果。".format \
            (index) + res.strip() + "\n" + "对该搜索结果进行总结，然后回答问题：{}。如果你无法找到问题的答案，则不需要返回总结的结果，仅简单的返回结果即可。".format \
            (messages)
        content[-1]["content"]=i_say
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                                messages=content,
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


# 画图插件
def generate_dalle(key,message):
    openai.api_key = key
    messages = message[-1]["content"]
    res = openai.Image.create(
        prompt=messages,
        n=1,
        size="256x256"
    )

    reply_content = "请及时保存，一段时间该图片将被删除\n\n" + "![图像描述]({})".format(
        res['data'][0]['url'])
    response_content["choices"][0]["delta"]["content"] = reply_content
    yield f'data: {json.dumps(response_content)}\n\n'
    yield 'data: {"choices": [{"delta": {"content": "[DONE]\n"}}]}\n\n'


# 文心一言插件
def generate_baidu(key,message):
    messages = message[-1]["content"]
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={}".format(key)

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

    response = requests.request("POST", url, headers=headers, data=payload, stream=True)
    for R in response.iter_lines():
        if R:
            rep = R.decode('utf-8')
            cont = json.loads(rep[6:])["result"]
            for c in cont:
                time.sleep(0.05)
                # print(c, end="", flush=True)
                response_content["choices"][0]["delta"]["content"] = c
                yield f'data: {json.dumps(response_content)}\n\n'

    yield 'data: {"choices": [{"delta": {"content": "[DONE]"}}]}\n\n'


