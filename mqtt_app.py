__author__ = "madawood"

# !/usr/bin/python
import time
import signal
import os
import logging

from ConfigParser import SafeConfigParser
from mqtt_sub import MqttSub
from dweet import Dweet
from cloud import Cloud

logger = logging.getLogger("mqtt_app")

from logging.handlers import RotatingFileHandler


def _sleep_handler(signum, frame):
    print "SIGINT Received. Stopping app"
    raise KeyboardInterrupt


def _stop_handler(signum, frame):
    print "SIGTERM Received. Stopping app"
    raise KeyboardInterrupt


signal.signal(signal.SIGTERM, _stop_handler)
signal.signal(signal.SIGINT, _sleep_handler)

DISPLAY_MSG = "Hello! Welcome!"
OUTPUT = dict()

# Get hold of the configuration file (package_config.ini)
moduledir = os.path.abspath(os.path.dirname(__file__))
BASEDIR = os.getenv("CAF_APP_PATH", moduledir)
tcfg = os.path.join(BASEDIR, "package_config.ini")

CONFIG_FILE = os.getenv("CAF_APP_CONFIG_FILE", tcfg)

cfg = SafeConfigParser()
cfg.read(CONFIG_FILE)


def setup_logging(cfg):
    """
    Setup logging for the current module and dependent libraries based on
    values available in config.
    """
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

    # Set log level based on what is defined in package_config.ini file
    loglevel = cfg.getint("logging", "log_level")
    logger.setLevel(loglevel)

    # Create a console handler only if console logging is enabled
    ce = cfg.getboolean("logging", "console")
    if ce:
        console = logging.StreamHandler()
        console.setLevel(loglevel)
        console.setFormatter(formatter)
        # add the handler to the root logger
        logger.addHandler(console)

    # The default is to use a Rotating File Handler
    log_file_dir = os.getenv("CAF_APP_LOG_DIR", "/tmp")
    log_file_name = cfg.get("logging", "filename")
    log_file_path = os.path.join(log_file_dir, log_file_name)

    # Lets cap the file at 1MB and keep 3 backups
    rfh = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024, backupCount=3)
    rfh.setLevel(loglevel)
    rfh.setFormatter(formatter)
    logger.addHandler(rfh)


if __name__ == '__main__':
    setup_logging(cfg)

    cloud_enabled = cfg.getboolean("cloud", "enabled")
    cloud_server = cfg.get("cloud", "server")
    cloud_port = cfg.get("cloud", "port")
    cloud_url = cfg.get("cloud", "url")
    cloud_time_out = cfg.getint("cloud", "time_out")
    cloud = Cloud(cloud_enabled, cloud_server, cloud_port, cloud_url, timeout=cloud_time_out)

    enabled = cfg.getboolean("dweet", "enabled")
    dweet_server = cfg.get("dweet", "server")
    dweet_name = cfg.get("dweet", "name")
    dweet_time_out = cfg.getint("dweet", "time_out")
    dweet = Dweet(enabled, dweet_server, dweet_name, timeout=dweet_time_out)

    broker_host = cfg.get("mqtt_broker", "host")
    broker_port = cfg.get("mqtt_broker", "port")

    sub_enabled = cfg.getboolean("mqtt_subscribe", "enabled")
    sub_topics = cfg.get("mqtt_subscribe", "topics")
    sub_topics = sub_topics.split(",")
    sub_time_out = cfg.getint("mqtt_subscribe", "time_out")
    sub = MqttSub(sub_enabled, broker_host, broker_port, sub_topics, timeout=sub_time_out)
    sub.start()
    time.sleep(3)


    def terminate_self():
        logger.info("Stopping the application")
        try:
            sub.close()
        except Exception as ex:
            logger.exception("Error stopping the app gracefully. Cause: %s" % ex.message)
        sub.join(timeout=5)
        logger.info("Killing self..")
        os.kill(os.getpid(), 9)


    while True:
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            terminate_self()
            break
        except Exception as ex:
            logger.exception("Caught exception! Terminating..")
            terminate_self()
            break
