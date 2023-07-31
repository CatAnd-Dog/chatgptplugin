# Description: Configuration file for the project

# 总开关
oneperfect = {
    "poe": False,  # 是否开启poe逆向功能
    "poe-online": False,  # 是否开启poe逆向联网功能------不建议开启，因为poe联网和3.5联网没有太大的区别，而且poe联网的速度慢，也容易封号
    "gpt-online": True,  # 是否开启gpt-3.5 的联网功能
    "gpt-image": True,  # 是否开启gpt 的画图功能
    "baidu-wxyy": True,  # 是否开启百度文心一言功能
    "wxyy-continue": False,  # 是否开启百度文心一言的连续对话功能（上下文记忆）---可能会有大量的token消耗
    "gpt-plugins": False,  # 是否开启gpt 的插件功能
    "newbing": False,  # 是否开启必应功能-----不要动，还没做好
    "mj": False,  # 是否开启mj画图功能-----不要动，还没做好
    "minimax": True,
    "minimax_continue": True,
    "mini_api_key": "",  # MiniMax API Key
    "mini_group_id": "",  # MiniMax Group ID
    "mini_access_key": "",  # 鉴权Key
}

# 支持二次中转的api地址。谨慎修改。最后面的  /   一定要加上
baseurl = "https://api.openai.com/"

# prompt 提示词部分
content_online_keyword = [
    {
        "name": "get_current_weather",
        "description": "获取浏览器搜索关键词",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "获取用户的关键词信息，用作浏览器搜索。"
                }
            },
            "required": ["keyword"]
        }
    }
]  # 联网功能--提取用户的搜索关键词
content_online_reply = [{"role": "system",
                         "content": "请从以下给定的搜索结果中抽取信息，并对搜索结果进行总结，然后回答问题。如果你无法找到问题的答案，则不需要返回总结的结果，仅简单的返回结果即可。"},
                        {"role": "user", "content": ""}
                        ]  # 联网功能--总结联网搜索的结果
content_plugins = [
    {
        "name": "get_current_weather",
        "description": "获取用户的意图和关键词信息",
        "parameters": {
            "type": "object",
            "properties": {
                "intent": {
                    "type": "string",
                    "enum": ["听歌", "看电影"]
                },
                "keyword": {
                    "type": "string",
                    "description": "获取用户的关键词信息，如果是听歌，就是歌手或者歌手名名，如果是看电影，就是演员或者电影名。需要根据用户的意图来判断，如果需要推荐，则给出推荐。"
                }
            },
            "required": ["intent", "keyword"]
        }
    }
]  # 插件功能区--分析用户的意图，然后返回对应的搜索关键词

# 联网搜索引擎选择 0：谷歌 google.com  1：https://lite.duckduckgo.com/lite --我也不知道这个是什么，别人推荐的
online = 0

# 娱乐插件功能,
happy = {
    "proxy": "",  # 国外可能无法使用，需要代理回国
    "music": True,  # 是否开启音乐功能
    "movie": False,  # 是否开启电影功能---没做好
}

# poe 逆向功能
poe = {

    "poe_ck": [""],
    # poe 的cookie  # poe_ck=["ck1","ck2","ck3","ck4"]。如果开启poe逆向功能，cookie值需要填写大于等于4个。会自动检测失效的cookie，并替换失效的cookie。
    "poe_apikey": "",  # poe 逆向 apikey  ，如果不需要这个密码功能，可以不填
    "poe_botname": {
        "Claude-instant-100k": "a2_100k",
        "sage": "capybara",
        "Claude-2-100k": "a2_2",
        "gpt-4": "beaver",
        "Claude-instant": "a2",
        "google-bot": "acouchy",
        "gpt-4-32k": "beaver",
        "gpt-GPT-4": "beaver",
    },  # poe 逆向 机器人的名字        左边是模型名字，右边是机器人名字。

}

newbing_ck = ""  # newbing 的cookie
