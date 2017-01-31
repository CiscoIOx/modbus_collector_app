__author__ = "madawood"

import logging
import httplib
import signal
import json

logger = logging.getLogger("mqtt_app")


def _sleep_handler(signum, frame):
    print "SIGINT Received. Stopping app"
    raise KeyboardInterrupt


def _stop_handler(signum, frame):
    print "SIGTERM Received. Stopping app"
    raise KeyboardInterrupt


class Dweet(object):
    __singleton = None  # the one, true Singleton
    __singleton_init_done = False

    def __new__(cls, *args, **kwargs):
        # Check to see if a __singleton exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __singleton objects
        if cls != type(cls.__singleton):
            # if not cls.__singleton:
            cls.__singleton = super(Dweet, cls).__new__(cls, *args, **kwargs)
        return cls.__singleton

    def __init__(self, enabled=True, server="dweet.io", name=None, timeout=5):
        self.enabled = enabled
        self.server = server
        self.name = name
        self.timeout = timeout
        logger.debug("Initialized the Dweeting !!")

    def dweet(self, content):
        if self.enabled:
            try:
                logger.debug("Connecting to https://%s", self.server)
                conn = httplib.HTTPSConnection(self.server, timeout=self.timeout)
                # params = urllib.urlencode(content)
                url = "/dweet/for/%s" % (self.name)
                logger.debug("Dweeting: %s", url)
                conn.request("POST", url, body=json.dumps(content), headers={'Content-Type': 'application/json'})
                response = conn.getresponse()
                logger.debug("Response Status: %s, Response Reason: %s", response.status, response.reason)
            except Exception as ex:
                logger.error("Exception while dweeting: cause: %s" % ex.message)

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
    m = Dweet(name="awake-transport")
    for i in range(5):
        m.dweet(content)
