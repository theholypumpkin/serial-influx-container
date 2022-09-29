# serial-influx-container
**Motto: keep it simple keep it stupid :)**

This is a quick and dirty python script which read out a json object recived on a serial interface and parses it to influxdb.
For example you want to read in data, from a Arduino.
## Getting started.
- Clone this repo
- Create the config
- Build the container
- run the container
### Well how to:
- rename the file called ```sample_config.yml``` to ```influxserial.yml``` and enter your configuration.
```yml
devices:
  device_name_1:                #you can name this tag how you want like "when pigs fly"
    interface: /dev/tty1        #your serial interface name
    baud: 9600                  #your baud rate
    bucket: my_bucket           # your influxdb2 bucket
    org: my_org                 # your influxdb2 org
    token: my_token             # your token, choose wisely. A good token for this program CAN ONLY WRITE to the your bucket!         
    url: https://your_influxdb_server.org
    port: 12345                 # when using the default 8086 port for influx db, this tag can be obmitted
```
__Note: because my server runs fedora, I use podman instead of docker.__
Just replace ```podman``` with ```docker``` and it should be fine.
```sh
sudo podman build -f influx_serial.dockerfile -t theholypumpkin/serial-influx .
sudo podman run --name=serial-influx -d --device /dev/ttyACM0:/dev/ttyACM0 --group-add dialout --restart unless-stopped localhost/theholypumpkin/serial-influx:latest
```
__Yes in this case we will build and run the container as root, which is considered unsafe.__ But because we have no exposed ports, we should be fine. If the system get compromised but you choose a good token, the attacker could only write junk data to your database.
If you do not like to run as root you can play around with premissions and for the device access and much more.

# Potential issues:
- you get repeated serial readings? This is an issue with pySerial and you USB-Controller or Serial-Chip. We flush the input buffer after every successful read but in some cases the buffer on the controller itself is not flushed.

# Addional material:
- There is Ardino Sample Code to test this container.