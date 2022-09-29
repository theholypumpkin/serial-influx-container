# read a serial data stream and send the data to influxdb
from serial import Serial
import json
import logging
import yaml
import influxdb_client
from datetime import datetime
from influxdb_client.client.write_api import SYNCHRONOUS
from meteocalc import heat_index, Temp
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)
logging.debug("opening config")
with open('influxserial.yml', 'r') as config_file:
        logging.debug("config loaded")
        data = yaml.safe_load(config_file)

# if multiple devices are specified
for device_name in data["devices"]:
    INTERFACE = data["devices"][str(device_name)].get("interface")
    BAUD = data["devices"][str(device_name)].get("baud")
    BUCKET = data["devices"][str(device_name)].get("bucket")
    ORG = data["devices"][str(device_name)].get("org")
    TOKEN = data["devices"][str(device_name)].get("token")
    URL = data["devices"][str(device_name)].get("url")
    logging.debug("config parsed")
    
    # Start the serial port
    while True:
        try:
            with Serial(INTERFACE, BAUD) as serial:
                line = serial.readline() # read until \n, wait indefinitly
                serial.reset_input_buffer() # flush the input buffer 
                message = json.loads(line)
                logging.debug("new message arrived")
            
            temperature = Temp(message['fields']['temperature']) # default value for 2nd param is Celsius
            humidity = message['fields']['humidity']
            heatindex = heat_index(temperature, humidity)
            heatindex = round(heatindex._convert_to('c'), 2) # works but uses private method
            message['fields']['heat index'] = heatindex
            message['time'] = str(datetime.utcnow())
            logging.debug("appended message")
    
            client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
            with client.write_api(write_options=SYNCHRONOUS) as write_api:
                write_api.write(bucket=BUCKET,org=ORG, record=message)
            logging.debug(message)
        except json.decoder.JSONDecodeError as e:
            logging.warning("JSON is improperly formated, can't be decoded")
            logging.warning(e)
        except influxdb_client.rest.ApiException as e:
            logging.warning("influxdb api execption")
            logging.warning(e)
        except serial.serialutil.SerialException as e:
            logging.warning("Can not open serial port")
            logging.warning(e)
        except Exeception as e:
            logging.error(e)


