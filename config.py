# Description: Configuration file for the project

# 总开关
oneperfect={
"poe" : False ,  # 是否开启poe逆向功能
"poe-online" : False ,  # 是否开启poe逆向联网功能------不建议开启，因为poe联网和3.5联网没有太大的区别，而且poe联网的速度慢，也容易封号
"gpt-online": True ,  # 是否开启gpt-3.5 的联网功能
"gpt-image": True ,  # 是否开启gpt 的画图功能
"baidu-wxyy": True ,  # 是否开启百度文心一言功能
"gpt-plugins": False ,  # 是否开启gpt 的插件功能-----不要动，还没做好
"newbing": False ,  # 是否开启必应功能-----不要动，还没做好
"mj": False ,  # 是否开启mj画图功能-----不要动，还没做好
}


# 支持二次中转的api地址。谨慎修改。最后面的  /   一定要加上
baseurl="https://api.openai.com/"



# prompt 提示词部分
content_online_keyword=[{"role": "system","content": "你是一个聪明的浏览器搜索小助手，你需要分析 用户的消息，并给出合理的浏览器搜索关键词。你仅需要返回适合浏览器搜索的关键词，不需要返回任何其他的消息。"},
                 {"role": "user", "content": "你好，请告诉我今天谷歌的股价是多少?"},
                  {"role": "assistant", "content": "谷歌股价"},
                  {"role": "user", "content": ""},
                  ]   # 联网功能--提取用户的搜索关键词
content_online_reply=[{"role": "system","content": "请从以下给定的搜索结果中抽取信息，并对搜索结果进行总结，然后回答问题。如果你无法找到问题的答案，则不需要返回总结的结果，仅简单的返回结果即可。"},
                        {"role": "user", "content": ""}
                       ]   # 联网功能--总结联网搜索的结果
content_plugins=[{"role": "system","content": "你是一个聪明的搜索小助手，你可以分析用户的意图以及提取相应的关键词信息。 用户的意图只能包含：听音乐，看电影这两种。 你需要根据用户的意图提取关键词，如果用户的意图是听音乐，你需要提取相应的歌名或者歌手名。如果用户的意图是看电影，你需要提取相应的电影名或者演员名。当你无法直接提取相应的关键词时，你需要根据用户的意图和内容推荐出相关性最大的歌名或者电影名。 ​你的意图只能是听音乐，看电影这两种中的其中一个，如果你实在无法分析出意图，则默认为听音乐。 我会给你几个示例，你需要按照示例进行回答。"},
                 {"role": "user", "content": "你好，我想听周杰伦的稻香。"},
                  {"role": "assistant", "content": "意图：听歌。关键词：稻香"},
                    {"role": "user", "content": "你好，我记得有一首圣斗士星矢的主题曲，他是一首非常好听的日漫歌曲"},
                  {"role": "assistant", "content": "意图：听歌。关键词：极乐净土"},
                    {"role": "user", "content": "你好，我想看肖申克的救赎"},
                  {"role": "assistant", "content": "意图：看电影。关键词：肖申克的救赎"},
                  {"role": "user", "content": ""},
                  ]   # 插件功能区--分析用户的意图，然后返回对应的搜索关键词


# poe 逆向功能
poe={

     "poe_ck":[""],   # poe 的cookie  # poe_ck=["ck1","ck2","ck3","ck4"]。如果开启poe逆向功能，cookie值需要填写大于等于4个。会自动检测失效的cookie，并替换失效的cookie。
    "poe_apikey":"",  # poe 逆向 apikey  ，如果不需要这个密码功能，可以不填
    "poe_botname":{
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

newbing_ck=""     # newbing 的cookie



