from time import sleep
from json import dumps
from kafka import KafkaProducer
import requests

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))

print("Fetching Data from Purple Air sensors")

def get_sensor_details(sensor):
    headers = {"X-API-Key": "E81E65A8-65EC-11ED-B5AA-42010A800006"}
    url = f"https://api.purpleair.com/v1/sensors/{sensor}"
    response = requests.get(url, headers=headers)
    
    return response

# sensor list 
sensor_list = ["128679", "42145", "103092", "33861", "72009", "149716", "147691", "120351", "158823", "142906", "133099", "103358", "158823", "137008", "128591", "131379"]

response_list = []

for sensor in sensor_list:
   data = get_sensor_details(sensor).json()
   producer.send('air-quality', value=data)
   print(f"Sending sensor data : {sensor}")
   sleep(1)
