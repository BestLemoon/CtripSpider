# CtripSpider
Ctrip Airlines Spider with verification cracker

##2020-12-30更新
由于Ctrip主站反爬机制更新，现在从m.ctrip.com入手更新了整套系统。



## 免责声明：
**本项目仅供技术交流，遵循robots.txt且仅对公开信息做了爬取，任何二次开发的盈利与本项目无关，若侵犯了贵公司的权益，请联系我删除。[email](mailto:admin@lemoon.ml)**


## 如何运行：

```python
pip install -r requiremens.txt
python main.py
```

在运行之前，请务必自行修改/填充main.py和send_messages.py里面的信息**请尽可能不要使用一个ip去爬取多架航班的数据，可能会造成程序之间的运行混乱**

## 实现的功能：
1.监控具体某一天的**一架航班**的价格和余票并且通过wechat和email提醒，若需更多天或者更多航班架次可以自行进行再次开发
2.自动识别验证码，包括滑动验证码和点击文字验证码（调用Tencent OCR api）,也可自行替换为baidu ocr

## TodoList
- [ ] 一架航班的长期监控
- [ ] 同一天多架航班同时监控
- [ ] 往返航班的监控
...
咕咕咕，个人暂时没有以上需求，若有需求可以联系我


