# read a serial data stream and send the data to influxdb
from serial import Serial
import json
import logging
import yaml
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from meteocalc import heat_index, Temp
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def read_and_send():
    pass
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
    while True:
        try:
            with Serial(INTERFACE, BAUD) as serial:
                line = serial.readline() # read until \n, wait indefinitly
                message = json.loads(line)
            # with open('sample_json_2.json', 'r') as line:
            #    message = json.load(line)
            
            temperature = Temp(message['fields']['temperature']) # default value for 2nd param is Celsius
            humidity = message['fields']['humidity']
            heatindex = heat_index(temperature, humidity)
            heatindex = round(heatindex._convert_to('c'), 2) # works but uses private method
            message['fields']['heat index'] = heatindex

            
            
            client = influxdb_client.InfluxDBClient(
                url=URL,
                token=TOKEN,
                org=ORG
            )

            with client.write_api(write_options=SYNCHRONOUS) as write_api:
                write_api.write(bucket=BUCKET,org=ORG, record=message)
            print(message)
        except json.decoder.JSONDecodeError as e:
            print('JSON Error')
        finally:
            message = None


