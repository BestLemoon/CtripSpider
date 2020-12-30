from send_messages import *
from Get_Infos import CtripSpider
import time

if __name__ == "__main__":
    spider = CtripSpider(dcityname="重庆", acityname="北京", date="2021-01-14", flightnumber='3U8822', price=300,
                         seat=5)
    # price为价格阈值，seat为余票阈值
    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        status, price, seat = spider.get_infos()
        if status:
            messages = ''
            if status == 1:
                messages = "机票降价啦~~\n现在价格是：" + str(price)
            elif status == 2:
                messages = "机票要被抢完咯~~\n当前仅剩" + str(seat) + "张票啦~~"
            send_wechat_messages(messages)
            break
        # time.sleep(30)
