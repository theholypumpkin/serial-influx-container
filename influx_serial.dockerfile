# syntax=docker/dockerfile:1
FROM python:bullseye
WORKDIR /usr/src/app
RUN pip install --no-cache-dir pyserial influxdb-client ruamel.yaml
COPY . .
CMD [ "python","./scripy.py" ]