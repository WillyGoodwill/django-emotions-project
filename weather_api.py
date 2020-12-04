import requests
import json
s_city = "Saint Petersburg,RU"
# s_city = "Amsterdam,NL"
# s_city = "Almere,NL"

city_id = 0
appid = "e39c82d8879b82213e1312de1f211aa5"
# try:
res = requests.get("http://api.openweathermap.org/data/2.5/find",params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
data = res.json()


cities = ["{} ({})".format(d['name'], d['sys']['country']) for d in data['list']]
print("city:", cities)
city_id = data['list'][0]['id']
print('city_id=', city_id)
# except Exception as e:
#     print("Exception (find):", e)
#     pass

# try:
# city_id = 498817    
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
json_object = json.dumps(data, indent = 4) 

with open("weather.json", "w") as outfile: 
    outfile.write(z) 
    
print("conditions:", data['weather'][0]['description'])
print("temp:", data['main']['temp'])
print("temp_min:", data['main']['temp_min'])
print("temp_max:", data['main']['temp_max'])
except Exception as e:
    print("Exception (weather):", e)
    pass

import datetime
def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

x=[]
y = {'currenttime':datetime.datetime.now(),
    'temperature':data['main']['temp']
    }
y2 = {'currenttime':datetime.datetime.now(),
    'temperature':data['main']['temp']
    }


x.append(y2)

z = json.dumps(x,sort_keys=True,
  indent=1,
  default=default)