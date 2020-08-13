import requests
import json

# 爬取城市简称和机场缩写
def get_city_infos():
    city_infos = {}
    url = 'https://flights.ctrip.com/itinerary/api/poi/get'
    r = requests.get(url)
    city_json = json.loads(r.text)
    for i in city_json['data']:
        cities = city_json['data'][i]
        if type(cities) == dict:
            for j in cities.items():
                for k in j:
                    if type(k) == list:
                        for m in k:
                            # print(m)
                            city_infos[m['display']] = m['data'][-3:]
    return city_infos
