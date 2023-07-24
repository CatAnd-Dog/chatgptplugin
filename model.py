from func  import online
from func.happyplugin import get163
from func.movies import get_movie_list,get_move_iframe
import openai
import json
import config
import requests
import time



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


def generate_function(message,funcion):

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                            messages=[ {"role": "user", "content": message}],
                                            functions=funcion,
                                            temperature=1,
                                            top_p=0.8, frequency_penalty=0,
                                            presence_penalty=0,
                                            )
    try:
        return response["choices"][0]["message"]["function_call"]["arguments"]
    except:
        return {"intent":"无法识别","keyword":"oneperfect.cn"}


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
    function=config.content_online_keyword
    messages=generate_function(message[-1]["content"],function) # 获取最后一条消息,并进行关键词提取
    keyword=json.loads(messages)["keyword"]
    if keyword == "":
        keyword = "排行榜"
    print(keyword)
    content=config.content_online_reply
    urls = online.google(keyword)
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

            response_content["choices"][0]["delta"]["content"] = "\n\n\n[第{}条搜索结果]({})\n".format(index,url['link'])
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
        for c in "【oneperfect】跟我一起来听歌【oneperfect】<br>":
            time.sleep(0.05)
            response_content["choices"][0]["delta"]["content"] = c
            yield f'data: {json.dumps(response_content)}\n\n'
        music = f"""<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=auto height==auto src="//music.163.com/outchain/player?type=2&id={s[2:]}&auto=0&height=auto"></iframe><br>发送音乐+id，即可切换歌曲，比如：音乐5257138<br>版权标识为1则无法听歌"""
        response_content["choices"][0]["delta"]["content"] = music
        yield f'data: {json.dumps(response_content)}\n\n'

    elif s.startswith("电影") :
        for c in "【oneperfect】跟我一起来看电影【oneperfect】<br>":
            time.sleep(0.05)
            response_content["choices"][0]["delta"]["content"] = c
            yield f'data: {json.dumps(response_content)}\n\n'
        try:
            bb = get_move_iframe(s[2:])
            ss = '<iframe allowfullscreen="true" border="0" frameborder="0" marginheight="0" marginwidth="0" scrolling="no" src="{}" width="650px" height="400px" ></iframe>'.format(
                bb)
        except:
            ss = "没有找到该电影，请检查一下输入是否正确。例：电影383/play-731813"
        response_content["choices"][0]["delta"]["content"] = ss
        yield f'data: {json.dumps(response_content)}\n\n'

    else:
        function = config.content_plugins     # 获取插件函数
        message=generate_function(s,function) # 获取插件函数返回的消息
        intent=json.loads(message)["intent"]
        keyword=json.loads(message)["keyword"]
        print(intent,keyword)

        if intent == "听歌":
            response_content["choices"][0]["delta"]["content"] = "【oneperfect】跟我一起来听歌<br>"
            yield f'data: {json.dumps(response_content)}\n\n'
            if keyword == "":
                pass
            else:
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
            response_content["choices"][0]["delta"]["content"] = "【oneperfect】跟我一起来看电影。发送电影+id，即可开始播放，比如：电影383/play-731813<br>"
            yield f'data: {json.dumps(response_content)}\n\n'
            s = '<style> .wrapper { display: flex;flex-wrap: wrap; list-style: none; padding: 0; margin: 0; }  .wrapper li {  width: calc(100% / 3);  text-align: center; margin-bottom: 10px; }.wrapper ul { padding: 0;  margin: 0; list-style: none;} .wrapper ul li { margin-bottom: 5px; }</style><ul class="wrapper">'

            if keyword == "":
                s = "没有识别到你的电影名，请重新输入。"
            else:
                try:
                    data=get_movie_list(keyword)
                except:
                    data=[[["//img.y80s.tv/upload/img/201608/383.jpg","没有找到该电影{}，请检查一下输入是否正确。".format(keyword)],[""]]]
                for i in data:
                    s += '<li><img src="{}" width="100px" ><br>'.format(i[0][0]) + i[0][1] + "<br>"
                    for j in i[1]:
                        s +="<p>" + j + "</p>"
                    s += "</li>"
                s += "</ul>"
            response_content["choices"][0]["delta"]["content"] = s
            yield f'data: {json.dumps(response_content)}\n\n'






# 其他模型---官网转发
def  generate_others(key,message):
    openai.api_key = key
    pass

