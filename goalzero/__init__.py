"""
Goal Zero Rest Api
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2020 by Robert Hillis.
Not affiliated with Goal Zero. Credit for headers belongs to Goal Zero.
:license: Apache 2.0, see LICENSE for more details.
"""
import aiohttp
from . import exceptions

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
            async with self._session.get(
                "http://" + self.host + "/state", timeout=TIMEOUT
            ) as response:

                self.data = await response.json()
                if "thingName" in self.data:
                    return self.data
                else:
                    raise exceptions.InvalidHost()
        except aiohttp.client_exceptions.ClientConnectorError:
            raise exceptions.ConnectError() from aiohttp.client_exceptions.ClientConnectorError

    async def post_state(self):
        """Post payload to Goal Zero Yeti instance."""
        async with self._session.post(
            "http://" + self.host + "/state",
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ) as request:
            self.data = await request.json()
        return self.data

    async def sysinfo(self):
        """Get system info from Goal Zero Yeti instance."""
        endpoint = "/sysinfo"
        async with self._session.get(
            "http://" + self.host + endpoint, timeout=TIMEOUT
        ) as response:
            self.data = await response.json()
        return self.data

    async def reset(self):
        """Reset Goal Zero Yeti instance."""
        self.payload = {}
        endpoint = "/factory-reset"
        async with self._session.post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ) as request:
            self.data = await request.json()
        return self.data

    async def reboot(self):
        """Reboot Goal Zero Yeti instance."""
        endpoint = "/rpc/Sys.Reboot"
        async with self._session.get(
            "http://" + self.host + endpoint, timeout=TIMEOUT
        ) as response:
            self.data = await response.json()
        return self.data

    async def get_loglevel(self):
        """Get log level Goal Zero Yeti instance."""
        endpoint = "/loglevel"
        async with self._session.get(
            "http://" + self.host + endpoint, timeout=TIMEOUT
        ) as response:
            self.data = await response.json()
        return self.data

    async def post_loglevel(self):
        """Post log level Goal Zero Yeti instance."""
        endpoint = "/loglevel"
        async with self._session.post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ) as request:
            self.data = await request.json()
        return self.data

    async def join(self):
        """Join Goal Zero Yeti instance to Wifi network."""
        endpoint = "/join"
        async with self._session.post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ) as request:
            self.data = await request.json()
        return self.data

    async def wifi(self):
        """Get available Wifi networks visible to Goal Zero Yeti instance."""
        endpoint = "/wifi"
        async with self._session.get(
            "http://" + self.host + endpoint, timeout=TIMEOUT
        ) as response:
            self.data = await response.json()
        return self.data

    async def password_set(self):
        """Set password to Zero Yeti instance."""
        self.payload = {"new_password": "" + self.payload + ""}
        endpoint = "/password-set"
        async with self._session.post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ) as request:
            self.data = await request.json()
        return self.data

    async def join_direct(self):
        """Directly Join Goal Zero Yeti instance on its Wifi."""
        self.payload = {}
        endpoint = "/join-direct"
        async with self._session.post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ) as request:
            self.data = await request.json()
        return self.data

    async def start_pair(self):
        """Pair with Goal Zero Yeti instance."""
        self.payload = {}
        endpoint = "/start-pair"
        async with self._session.post(
            "http://" + self.host + endpoint,
            json=self.payload,
            headers=HEADER,
            verify=False,
            timeout=TIMEOUT,
        ) as request:
            self.data = await request.json()
        return self.data
