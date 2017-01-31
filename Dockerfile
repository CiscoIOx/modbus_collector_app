FROM devhub-docker.cisco.com/iox-docker/base-x86_64
RUN opkg update
RUN opkg install python
RUN opkg install python-pip
RUN pip install paho-mqtt 
RUN pip install jsonschema 
RUN opkg remove python-pip
COPY mqtt_app.py /usr/bin/mqtt_app.py
COPY mqtt_sub.py /usr/bin/mqtt_sub.py
COPY dweet.py /usr/bin/dweet.py
COPY cloud.py /usr/bin/cloud.py
COPY package_config.ini /usr/bin/package_config.ini
CMD [“python”, “/usr/bin/mqtt_app.py”]
