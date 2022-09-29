# syntax=docker/dockerfile:1
FROM python:bullseye
WORKDIR /usr/src/app
RUN pip install --no-cache-dir pyserial influxdb-client meteocalc pyYAML
COPY . .
CMD [ "python","scripts.py" ]