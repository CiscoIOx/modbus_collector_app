import logging
import httplib
import signal
import json

logger = logging.getLogger("mqtt_app")
DATA = {}


def _sleep_handler(signum, frame):
    print "SIGINT Received. Stopping app"
    raise KeyboardInterrupt


def _stop_handler(signum, frame):
    print "SIGTERM Received. Stopping app"
    raise KeyboardInterrupt


class Cloud(object):
    __singleton = None  # the one, true Singleton
    __singleton_init_done = False

    def __new__(cls, *args, **kwargs):
        # Check to see if a __singleton exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __singleton objects
        if cls != type(cls.__singleton):
            # if not cls.__singleton:
            cls.__singleton = super(Cloud, cls).__new__(cls, *args, **kwargs)
        return cls.__singleton

    def __init__(self, enabled, server, port, url="/", method="POST", timeout=5):
        self.enabled = enabled
        self.server = server
        self.port = port
        self.url = url
        self.method = method
        self.timeout = timeout
        logger.debug("Initialized the Dweeting !!")

    def send_to_cloud(self, content):
        try:
            global DATA
            if self.enabled is False:
                logger.debug("Sending to data center app is disabled. Nothing to do...")
                return
            logger.debug("Connecting to http://%s:%s", self.server, self.port)

            conn = httplib.HTTPConnection(self.server, self.port, timeout=self.timeout)
            DATA.update(content)
            content = json.dumps(DATA)
            headers = {"Content-Type": "application/json"}
            logger.debug("Sending to cloud: URL %s, Headers %s, Body %s", self.url, headers, content)
            conn.request(self.method, self.url, content, headers)
            response = conn.getresponse()
            logger.debug("Response Status: %s, Response Reason: %s", response.status, response.reason)
        except Exception as ex:
            logger.exception("Error while sending a data to cloud. Cause: %s" % ex.message)

    @classmethod
    def get_instance(cls):
        '''
        Returns a singleton instance of the class
        '''
        if not cls.__singleton:
            return None
        return cls.__singleton


if __name__ == "__main__":
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    logger.setLevel(10)
    console = logging.StreamHandler()
    console.setLevel(10)
    console.setFormatter(formatter)
    logger.addHandler(console)

    signal.signal(signal.SIGTERM, _stop_handler)
    signal.signal(signal.SIGINT, _sleep_handler)
    content = {
        "key": "value"
    }
    c = Cloud(True, "10.78.106.222", "10001", "/")
    for i in range(5):
        c.send_to_cloud(content)
