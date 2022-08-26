# read a serial data stream and send the data to influxdb
import serial
import json
import logging
import yaml
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import math

def heat_index(temperature :float, percentHumidity: float):
    hi = 0.5 * (temperature + 16.1111 + ((temperature - 20)* 1.2)  +
              (percentHumidity * 0.094))
 
    if hi > 27:

        hi = math.fsum([
                        -8.784695,
                        1.61139411 * temperature,
                        2.338549 * percentHumidity,
                        -0.14611605 * temperature * percentHumidity,
                        -0.012308094 * (temperature ** 2),
                        -0.016424828 * (percentHumidity ** 2),
                        0.002211732 * (temperature ** 2) * percentHumidity,
                        0.00072546 * temperature * (percentHumidity ** 2),
                        -0.000003582 * (temperature ** 2) * (percentHumidity ** 2)
        ])
    
        if ((percentHumidity < 13) and (temperature >= 26.6667) and (temperature <= 44.4444)):
            hi -= ((13.0 - percentHumidity) * 0.25) * math.sqrt((17.0 - abs(temperature - 35.0)) * 0.05882)

        elif ((percentHumidity > 85.0) and (temperature >= 26.6667) and (temperature <= 30.5556)):
            hi += ((percentHumidity - 85.0) * 0.1) * ((30.5556 - temperature) * 0.2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def heat_index_fahrenheit(temperature, percentHumidity):
    hi = 0.5 * (temperature + 61.0 + ((temperature - 68.0) * 1.2) +
              (percentHumidity * 0.094));

    if hi > 79:
        hi = math.fsum([
                        -42.379,
                        2.04901523 * temperature,
                        10.14333127 * percentHumidity,
                        -0.22475541 * temperature * percentHumidity,
                        -0.00683783 * (temperature ** 2),
                        -0.05481717 * (percentHumidity ** 2),
                        0.00122874 *  (temperature ** 2) * percentHumidity,
                        0.00085282 * temperature * (percentHumidity ** 2),
                        -0.00000199 * (temperature ** 2) * (percentHumidity ** 2)
        ])

        if ((percentHumidity < 13) and (temperature >= 80.0) and (temperature <= 112.0)):
            hi -= ((13.0 - percentHumidity) * 0.25) * math.sqrt((17.0 - abs(temperature - 95.0)) * 0.05882)

        elif ((percentHumidity > 85.0) and (temperature >= 80.0) and (temperature <= 87.0)):
            hi += ((percentHumidity - 85.0) * 0.1) * ((87.0 - temperature) * 0.2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
with open('influxserial.yml', 'r') as config_file:
    data = yaml.safe_load(config_file)

# if multiple devices are specified
for device_name in data["devices"]:
    INTERFACE = data["devices"][str(device_name)].get("interface")
    BAUD = data["devices"][str(device_name)].get("baud")
    BUCKET = data["devices"][str(device_name)].get("bucket")
    ORG = data["devices"][str(device_name)].get("org")
    TOKEN = data["devices"][str(device_name)].get("token")
    URL = data["devices"][str(device_name)].get("url")
    
    # Start the serial port
    # with serial.Serial(INTERFACE, BAUD) as serial:
    #    line = serial.readLine() # read until \n
    #    message = json.loads(line)
    with open('sample_json_2.json', 'r') as line:
        message = json.load(line)
    
    temperature = message['fields']['temperature']
    humidity = message['fields']['humidity']
    heat_index(temperature, humidity)
    
    
    
#     client = influxdb_client.InfluxDBClient(
#     url=URL,
#     token=TOKEN,
#     org=ORG
# )

#     with client.write_api(write_options=SYNCHRONOUS) as write_api:
#         write_api.write(bucket=BUCKET,org=ORG, record=message)
#     print("Writen JSON")


