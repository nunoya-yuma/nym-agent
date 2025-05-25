# README

## Environment

```shell
uv sync
```

Before executing python-related commands, run the following commands to enter the virtual environment.

```shell
source .venv/bin/activate
```

## Math and weather agent

```shell
python src/mcp_servers/weather/weather_streamable_http.py
```

```shell
python -m src.agents.math_weather_agent
```

e.g.)

```log
$ python -m src.agents.math_weather_agent --provider=openai
Thread ID: e4f5a667-8347-4c24-9173-22051d1c9b48
Using model provider: openai
Processing request of type ListToolsRequest
================================ Human Message =================================

what's (3 + 5) x 12
================================== Ai Message ==================================
Tool Calls:
  multiply (call_3RJ9SbepoAJhfWZvUOXm1iEt)
 Call ID: call_3RJ9SbepoAJhfWZvUOXm1iEt
  Args:
    a: 8
    b: 12
Processing request of type CallToolRequest
================================= Tool Message =================================
Name: multiply

96
================================== Ai Message ==================================

The result of (3 + 5) x 12 is 96.
================================ Human Message =================================

I live in Osaka. Do you know where that is? (No need to search the web.)
================================== Ai Message ==================================

Yes, Osaka is a major city located in Japan. It's known for its modern architecture, nightlife, and delicious street food. Osaka is part of the Kansai region and is often considered the culinary capital of the country. Would you like to know more about Osaka or anything specific related to it?
================================ Human Message =================================

What is the weather at my current location?
================================== Ai Message ==================================
Tool Calls:
  get_weather (call_AN6YfRe83COYpjouRNNnh4SE)
 Call ID: call_AN6YfRe83COYpjouRNNnh4SE
  Args:
    location: Osaka
================================= Tool Message =================================
Name: get_weather

It's always sunny in Osaka!
================================== Ai Message ==================================

The weather in Osaka is currently sunny. If you need more specific information, such as temperature or forecasts, just let me know!
================================ Human Message =================================

Research one of today's Japanese news and tell me about it in Japanese.
================================== Ai Message ==================================
Tool Calls:
  tavily_search_results_json (call_3kcfI2xgNXRkjx8LUxgB8sSD)
 Call ID: call_3kcfI2xgNXRkjx8LUxgB8sSD
  Args:
    query: 日本の今日のニュース
================================= Tool Message =================================
Name: tavily_search_results_json

[{"title": "NHKニュース 速報・最新情報", "url": "https://www3.nhk.or.jp/news/", "content": "山口 下関で火災 複数の建物が燃える 6時31分\nススキノ男性殺害事件 母親に執行猶予付き有罪判決 札幌地裁 6時25分\n韓国 最大野党 前代表の裁判 6月3日の大統領選挙後に 6時24分\n塩野義製薬 JTの医薬品事業など約1600億円で買収へ 6時22分\n\n新着ニュース一覧を見る\n地域発ニュース\n首都圏のニュース\n\n埼玉 白岡市役所で火事 市の窓口業務はすべて休止 3時34分\n東京 杉並区 ブランド品買い取り店で５０００万円相当窃盗 4時05分\n神奈川 横須賀 多重衝突事故 “直前まで飲酒の可能性” 3時05分\n\n地域ニュース一覧を見る\n地図から選ぶ\n戻る\nClose Up\n\n関連ニュース 能登半島地震 最新情報\n関連ニュース フェイク対策\n特設サイト 感染症データと医療・健康情報\n特設サイト ウクライナ情勢\n特設サイト スペシャルコンテンツ一覧\n\nこちらもチェック", "score": 0.588062}, {"title": "JapaNews24 ～日本の最新ニュースを24時間ライブ配信 ... - YouTube", "url": "https://www.youtube.com/watch?v=coYw-eVU0Ks", "content": "JapaNews24 ～日本の最新ニュースを24時間ライブ配信　Japan News 24H  LIVE\nANNnewsCH\n4550000 subscribers\n\n191158034 views\n22 Jan 2019\n速報ニュースを中心に、事件や政治、自然災害など時事問題から街のトレンドまで24時間配信中！\n注目のニュースをまとめてお届けしています。\n\n#ライブ配信 #ニュース #テレ朝\n\n■テレ朝ニュース公式HP\nテレ朝news　https://news.tv-asahi.co.jp/\n\n■エンタメNews24 ～最新エンタメ情報を24時間配信\nhttps://youtube.com/live/4iJULMBT8_0\n\n■テレ朝ニュースSNS公式アカウント\nX(旧Twitter)　https://twitter.com/tv_asahi_news\nTikTok　https://www.tiktok.com/@tv_asahi_news\nFacebook　https://www.facebook.com/tvasahinews", "score": 0.560566}]
================================== Ai Message ==================================

今日、日本では以下のニュースが報じられています。

山口県下関で火災が発生し、複数の建物が燃えました。また、札幌地裁ではススキノの男性殺害事件に関連して、母親に執行猶予付きの有罪判決が下されました。

詳しい情報はNHKのページでご覧いただけます。[こちらから](https://www3.nhk.or.jp/news/)確認してください。
```
