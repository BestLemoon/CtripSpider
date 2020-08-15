import requests
from Get_Path import *
import re
import prettytable as pt
from Get_token import *
from Get_City_infos import *
from crack import crack

city_infos = get_city_infos()


class get_flight_info:
    def __init__(self, dcityname, acityname, date, flightnumber, price, seat):
        self.status = 0
        self.price = price
        self.flightnumber = flightnumber
        if seat is None:
            seat = 5
        self.seat = seat
        self.date = date
        self.acityname = acityname
        self.dcityname = dcityname
        self.dcity = city_infos.get(self.dcityname)
        self.acity = city_infos.get(self.acityname)
        self.token = get_token(self.dcityname, self.acityname)
        self.url = 'https://flights.ctrip.com/itinerary/api/12808/products'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            "content-type": "application/json",
            "referer": "https://flights.ctrip.com/itinerary/oneway/",
            "cookie": ""       #可在第一次破解反爬后加入到源码，减少以后触发反爬的次数
        }

        self.payload = {"flightWay": "Oneway",
                        "classType": "ALL",
                        "hasChild": "false",
                        "hasBaby": "false",
                        "searchIndex": 1,
                        "date": self.date,
                        "airportParams": [
                            {"dcity": self.dcity,
                             "acity": self.acity,
                             "dcityname": self.dcityname,
                             "acityname": self.acityname,
                             "date": self.date
                             }
                        ],
                        "token": self.token
                        }

    def get_infos(self):
        res = requests.post(self.url, data=json.dumps(self.payload), headers=self.headers).text
        print(res[:100])
        datas = json.loads(res)
        # print(type(datas))
        if datas["data"]["error"] is not None:
            print('开始破解反爬')
            cracker = crack()
            self.headers['cookie'] = cracker.main()
            print('破解完成')
            res = requests.post(self.url, data=json.dumps(self.payload), headers=self.headers).text
            print(res[:100])
            datas = json.loads(res)
        datas_paths = Get_Path(datas)
        raw_path = datas_paths.the_value_path(self.flightnumber)  # 匹配路径
        # print(raw_path)
        # print(type(raw_path))
        for path in raw_path:
            if 'sharedFlightNumber' in path:  # 去除共享航班
                continue
            raw_path = path
        # print(raw_path)
        routeList_num = re.compile(r'\d+').findall(raw_path)[0]
        # print(routeList_num)

        table = pt.PrettyTable()
        table.field_names = ["航空公司", "航班", "起飞时间-->到达时间", "准点率", "最低价格", "剩余座位"]

        flight_info = {}  # 存储信息
        raw_flight_info = datas['data']['routeList'][int(routeList_num)]['legs'][0]
        # print(raw_flight_info)
        flight_info['airlineName'] = raw_flight_info['flight']['airlineName']
        flight_info['FlightNumber'] = raw_flight_info['flight']['flightNumber']
        flight_info['time'] = raw_flight_info['flight']['departureDate'][-8:-3] + "-->" + raw_flight_info['flight'][
                                                                                              'arrivalDate'][-8:-3]
        flight_info['PunctualityRate'] = raw_flight_info['flight']['punctualityRate']
        lowest_price = raw_flight_info['characteristic']['lowestPrice']
        current_seat = raw_flight_info['cabins'][0]['seatCount']
        if lowest_price < self.price:
            self.status = 1
        elif current_seat <= self.seat:
            self.status = 2
        flight_info['lowestPrice'] = lowest_price
        flight_info['seatCount'] = current_seat

        # print(list(flight_info.values()))
        table.add_row(list(flight_info.values()))
        print(self.dcityname, '------->', self.acityname, self.date)
        print(table)
        return self.status, lowest_price, current_seat
