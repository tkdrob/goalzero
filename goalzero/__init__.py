"""
Goal Zero Rest Api
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2020 by Robert Hillis.
Not affiliated with Goal Zero. Credit for headers belongs to Goal Zero.
:license: Apache 2.0, see LICENSE for more details.
"""
import asyncio
import logging
import aiohttp
import async_timeout
from requests import get, post
from . import exceptions

_LOGGER = logging.getLogger(__name__)

HEADER = {
    "Content-Type": "application/json",
    "User-Agent": "YetiApp/1340 CFNetwork/1125.2 Darwin/19.4.0",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "Accept-Language": "en-us",
    "Content-Length": "19",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "no-cache",
}
TIMEOUT = 10


class GoalZero:
    """A class for handling connections with a Goal Zero Yeti."""

    def __init__(self, host, loop, session, **data):
        """Initialize the connection to Goal Zero Yeti instance."""
        self._loop = loop
        self._session = session
        self.host = host
        self.data = {}
        for key, value in data.items():
            if key == "payload":
                self.payload = value

    async def get_state(self):
        """Get states from Goal Zero Yeti instance."""
        try:
            async with async_timeout.timeout(10, loop=self._loop):
                response = get("http://" + self.host + "/state", timeout=TIMEOUT)

            _LOGGER.debug("Response from Goal Zero Yeti")
            self.data = response.json()
            _LOGGER.debug(self.data)
            return self.data
        except aiohttp.ClientError:
            msg = "Can not load data from Goal Zero Yeti: {}".format(self.host)
            _LOGGER.error(msg)
            raise exceptions.ConnectError(msg) from aiohttp.ClientError
        except asyncio.TimeoutError:
            msg = "Connection to Goal Zero Yeti timed out: {}".format(self.host)
            _LOGGER.error(msg)
            raise exceptions.ConnectError(msg) from asyncio.TimeoutError

    async def post_state(self):
        """Post payload to Goal Zero Yeti instance."""
        request = post(
            "http://" + self.host + "/state",
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ).json()
        return request

    async def sysinfo(self):
        """Get system info from Goal Zero Yeti instance."""
        endpoint = "/sysinfo"
        response = get("http://" + self.host + endpoint, timeout=TIMEOUT).json()
        return response

    async def reset(self):
        """Reset Goal Zero Yeti instance."""
        self.payload = {}
        endpoint = "/factory-reset"
        request = post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ).json()
        return request

    async def reboot(self):
        """Reboot Goal Zero Yeti instance."""
        endpoint = "/rpc/Sys.Reboot"
        response = get("http://" + self.host + endpoint, timeout=TIMEOUT).json()
        return response

    async def get_loglevel(self):
        """Get log level Goal Zero Yeti instance."""
        endpoint = "/loglevel"
        response = get("http://" + self.host + endpoint, timeout=TIMEOUT).json()
        return response

    async def post_loglevel(self):
        """Post log level Goal Zero Yeti instance."""
        endpoint = "/loglevel"
        request = post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ).json()
        return request

    async def join(self):
        """Join Goal Zero Yeti instance to Wifi network."""
        endpoint = "/join"
        request = post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ).json()
        return request

    async def wifi(self):
        """Get available Wifi networks visible to Goal Zero Yeti instance."""
        endpoint = "/wifi"
        response = get("http://" + self.host + endpoint, timeout=TIMEOUT).json()
        return response

    async def password_set(self):
        """Set password to Zero Yeti instance."""
        self.payload = {"new_password": "" + self.payload + ""}
        endpoint = "/password-set"
        request = post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ).json()
        return request

    async def join_direct(self):
        """Directly Join Goal Zero Yeti instance on its Wifi."""
        self.payload = {}
        endpoint = "/join-direct"
        request = post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ).json()
        return request

    async def start_pair(self):
        """Pair with" Goal Zero Yeti instance."""
        self.payload = {}
        endpoint = "/start-pair"
        request = post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ).json()
        return request
