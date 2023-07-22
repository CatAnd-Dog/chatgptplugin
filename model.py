from func  import online
from func.happyplugin import get163
import openai
import json
import config
import requests
import time
import re



# 全局变量
openai.api_base= config.baseurl+"v1"
wxyy_continue=config.oneperfect["wxyy-continue"]
happyplugine=config.happy

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

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                            messages=message,
                                            temperature=0.8,
                                            top_p=1, frequency_penalty=0,
                                            presence_penalty=0,
                                            )
    return response["choices"][0]["message"]["content"]


# 处理文心一言的连续对话问题
def wxyy_message(messages):
    if wxyy_continue:
        user_message=[{"role": "user","content":""},{"role": "assistant","content":""}]
        for index,word in  enumerate(messages):
            if word["role"]=="system":
                user_message[0]={"role": "user","content": word["content"]}
                user_message[1]= {"role": "assistant","content":"好的，我知道了"}

            elif word["role"]=="assistant" and messages[index-1]["role"]=="user":
                user_message.append({"role": "user", "content": messages[index-1]["content"]})
                user_message.append({"role": "assistant", "content": word["content"]})

        user_message.append({"role": "user", "content": messages[-1]["content"]})

    else:
        user_message=[
            {
                "role": "user",
                "content": messages[-1]["content"]
            }
        ]
    return  user_message

# 联网插件
def generate_online(key,message):

    openai.api_key = key
    content=config.content_online_keyword
    content[-1]["content"]=message[-1]["content"]
    messages=generate_openai(content) # 获取最后一条消息,并进行关键词提取
    print(messages)
    content=config.content_online_reply
    urls = online.google(messages)
    for index, url in enumerate(urls[:5]):
        res = online.scrape_text(url['link'])
        if res == "无法连接到该网页":
            pass
        i_say = "这是第{}条搜索结果。".format \
            (index) + res.strip() + "\n" + "对该搜索结果进行总结，然后回答问题：{}。如果你无法找到问题的答案，则不需要返回总结的结果，仅简单的返回结果即可。".format \
            (messages)

        content[-1]["content"]=i_say
        try:
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
        except:
            yield 'data: {"choices": [{"delta": {"content": "[DONE]\n"}}]}\n\n'
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

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={}".format(key)
    payload = json.dumps({
        "messages": wxyy_message(message),
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


# 娱乐插件
def  generate_plugin(key,message):
    openai.api_key = key
    s = message[-1]["content"]
    if s.startswith("音乐") and s[2:].isdigit():
        response_content["choices"][0]["delta"]["content"] = "【oneperfect】跟我一起来听歌<br>"
        yield f'data: {json.dumps(response_content)}\n\n'
        music = f"""<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=auto height==auto src="//music.163.com/outchain/player?type=2&id={s[2:]}&auto=0&height=auto"></iframe><br>发送音乐+id，即可切换歌曲，比如：音乐5257138<br>版权标识为1则无法听歌"""
        response_content["choices"][0]["delta"]["content"] = music
        yield f'data: {json.dumps(response_content)}\n\n'

    elif s.startswith("电影") and s[2:].isdigit():

        response_content["choices"][0]["delta"]["content"] = "还没有接入电影"
        yield f'data: {json.dumps(response_content)}\n\n'
    else:
        content = config.content_plugins
        content[-1]["content"] = s
        message=generate_openai(content)
        #message="意图：听歌。关键词：稻香"
        match = re.match(r'意图：(.*?)。关键词：(.*?)$', message)
        try:
            intent, keyword = match.group(1), match.group(2)
        except:
            intent, keyword = "无", "无"
        if intent == "听歌":
            response_content["choices"][0]["delta"]["content"] = "【oneperfect】跟我一起来听歌<br>"
            yield f'data: {json.dumps(response_content)}\n\n'
            reply = get163(keyword,happyplugine["proxy"])
            for r in reply:
                user_reply="歌名：{}，id：{}，版权：{}<br>".format(r[0],r[1],r[2])
                for c in user_reply:
                    response_content["choices"][0]["delta"]["content"] = c
                    yield f'data: {json.dumps(response_content)}\n\n'
                    time.sleep(0.03)

            music=f"""<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=auto height==auto src="//music.163.com/outchain/player?type=2&id={reply[0][1]}&auto=0&height=auto"></iframe><br>发送音乐+id，即可切换歌曲，比如：音乐5257138<br>版权标识为1则无法听歌"""
            response_content["choices"][0]["delta"]["content"] = music
            yield f'data: {json.dumps(response_content)}\n\n'

        if intent == "看电影":

            response_content["choices"][0]["delta"]["content"] = "还没有接入电影"
            yield f'data: {json.dumps(response_content)}\n\n'

        else:
            response_content["choices"][0]["delta"]["content"] = "不能识别用户的意图，请重新输入"
            yield f'data: {json.dumps(response_content)}\n\n'
    pass


# 其他模型---官网转发
def  generate_others(key,message):
    openai.api_key = key
    pass

