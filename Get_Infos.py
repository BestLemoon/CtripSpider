import requests
import json
import prettytable as pt
from Get_City_infos import get_city_infos
from Cracker import cracker


class CtripSpider():
    def __init__(self, dcityname, acityname, date, flightnumber, price, seat):
        city_infos = get_city_infos()
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
        self.url = 'https://m.ctrip.com/restapi/soa2/14022/flightListSearch'
        self.crack_url = f'https://m.ctrip.com/html5/flight/swift/domestic/{self.dcity}/{self.acity}/{self.date}'

    def get_data(self):
        data = {"preprdid": "", "trptpe": 1, "flag": 8,
                "searchitem": [{"dccode": self.dcity, "accode": self.acity, "dtime": self.date}], "subchannel": "null",
                "tid": "",
                "head": {"cid": "", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888", "syscode": "09",
                         "auth": "null",
                         "extension": [{"name": "aid", "value": "66672"}, {"name": "sid", "value": "1693366"},
                                       {"name": "protocal", "value": "https"}]}, "contentType": "json"}
        r = requests.post(self.url, data=json.dumps(data))
        FlightList = r.json()
        return FlightList

    def get_infos(self):
        global airlines
        airlines = ''
        FlightList = self.get_data()
        try:
            airlines = FlightList['airlines']
        except:
            print("开始破解")
            while airlines == '':
                cracker(self.crack_url)
                FlightList = self.get_data()
                airlines = FlightList['airlines']
        FlightList = self.get_data()
        fltitem = FlightList["fltitem"]
        table = pt.PrettyTable()
        table.field_names = ["航空公司", "航班", "起飞时间-->到达时间", "最低价格", "剩余座位"]
        flight_info = {}  # 存储信息

        for airline in airlines:
            if airline['aircode'] == self.flightnumber[:2]:
                flight_info['airlineName'] = airline['airsname']
                break
        for flight in fltitem:
            flgno = flight['mutilstn'][0]['basinfo']['flgno']
            if flgno == self.flightnumber:
                flight_info['FlightNumber'] = flgno
                flight_info['time'] = flight['mutilstn'][0]['dateinfo']['ddate'][-8:-3] + "-->" + \
                                      flight['mutilstn'][0]['dateinfo']['adate'][-8:-3]
                flight_info['lowestPrice'] = flight['policyinfo'][0]['priceinfo'][0]['price']
                flight_info['ticket'] = flight['policyinfo'][0]['priceinfo'][0]['ticket']
                break
        print(flight_info)
        if flight_info['lowestPrice'] < self.price:
            self.status = 1
        elif flight_info['ticket'] <= self.seat:
            self.status = 2

        # print(list(flight_info.values()))
        table.add_row(list(flight_info.values()))
        print(self.dcityname, '------->', self.acityname, self.date)
        print(table)
        return self.status, flight_info['lowestPrice'], flight_info['ticket']
