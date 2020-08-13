from send_messages import *
from get_flight_info import *
import time

if __name__ == "__main__":
    spider = get_flight_info(dcityname="杭州", acityname="北京", date="2020-09-01", flightnumber='AB1234',price=700, seat=3)
    while True:
        status, price, seat = spider.get_infos()
        if status:
            messages = ''
            if status == 1:
                messages = "机票降价啦~~\n现在价格是：" + str(price)
            elif status == 2:
                messages = "机票要被抢完咯~~\n当前仅剩" + str(seat) + "张票啦~~"
            send_email_messages(messages)
            send_wechat_messages(messages)
        # time.sleep(300)
