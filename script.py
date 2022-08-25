# read a serial data stream and send the data to influxdb
from urllib.error import URLError
import serial
import json
import logging
import yaml
import influxdb_client
import warnings
from influxdb_client.client.write_api import SYNCHRONOUS


infuxdb_point = "apartment_enviormental_data"

with open('influxserial.yml', 'r') as config_file:
    data = yaml.safe_load(config_file)

# if multiple devvices are specified
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
    with open('sample_json_file.json', 'r') as line:
        message = json.load(line)
    
    
    client = influxdb_client.InfluxDBClient(
    url=URL,
    token=TOKEN,
    org=ORG
)

    write_api = client.write_api(write_options=SYNCHRONOUS)

    data_point = influxdb_client.Point(infuxdb_point)

    for obj in message:
        if str(obj) == "tag": # extract tags
            for tag, value in message['tag'].items():
                data_point.tag(tag, value)
        else: # add data fields
            for field, value in message[str(obj)].items():
                data_point.field(field, value)
    
    write_api.write(bucket=BUCKET,org=ORG, record=data_point) 
    print("Data should be written")


