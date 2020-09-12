"""Goal Zero Rest Api."""

import aiohttp
from async_timeout import timeout
from . import exceptions

""":copyright: (c) 2020 by Robert Hillis.
Not affiliated with Goal Zero. Credit for headers belongs to Goal Zero.
:license: Apache 2.0, see LICENSE for more details."""


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


class Yeti:
    """A class for handling connections with a Goal Zero Yeti."""

    def __init__(self, host, loop, session, **data):
        """Initialize the connection to Goal Zero Yeti instance."""
        self._loop = loop
        self._session = session
        self.control = {}
        self.data = {}
        self.endpoint = {}
        self.host = host
        self.payload = {}
        for key, value in data.items():
            if key == "payload":
                self.payload = value

    async def get_state(self):
        """Get states from Goal Zero Yeti instance."""
        self.control = "thingName"
        self.endpoint = "/state"
        await Yeti.send_get(self)

    async def post_state(self):
        """Post payload to Goal Zero Yeti instance."""
        self.endpoint = "/state"
        await Yeti.send_post(self)

    async def sysinfo(self):
        """Get system info from Goal Zero Yeti instance."""
        self.endpoint = "/sysinfo"
        self.control = "name"
        await Yeti.send_get(self)

    async def reset(self):
        """Reset Goal Zero Yeti instance."""
        self.endpoint = "/factory-reset"
        await Yeti.send_get(self)

    async def reboot(self):
        """Reboot Goal Zero Yeti instance."""
        self.endpoint = "/rpc/Sys.Reboot"
        await Yeti.send_get(self)

    async def get_loglevel(self):
        """Get log level Goal Zero Yeti instance."""
        self.endpoint = "/loglevel"
        self.control = "app"
        await Yeti.send_get(self)

    async def post_loglevel(self):
        """Post log level Goal Zero Yeti instance."""
        self.endpoint = "/loglevel"
        await Yeti.send_post(self)

    async def join(self):
        """Join Goal Zero Yeti instance to Wifi network."""
        self.endpoint = "/join"
        await Yeti.send_post(self)

    async def wifi(self):
        """Get available Wifi networks visible to Goal Zero Yeti instance."""
        self.endpoint = "/wifi"
        await Yeti.send_get(self)

    async def password_set(self):
        """Set password to Zero Yeti instance."""
        self.payload = {"new_password": "" + self.payload + ""}
        self.endpoint = "/password-set"
        await Yeti.send_post(self)

    async def join_direct(self):
        """Directly Join Goal Zero Yeti instance on its Wifi."""
        self.endpoint = "/join-direct"
        await Yeti.send_post(self)

    async def start_pair(self):
        """Pair with Goal Zero Yeti instance."""
        self.endpoint = "/start-pair"
        await Yeti.send_post(self)

    async def send_get(self):
        """Send get request."""
        try:
            async with timeout(TIMEOUT, loop=self._loop):
                response = await self._session.get(
                    "http://" + self.host + self.endpoint
                )
                self.data = await response.json()
                if self.control not in self.data:
                    raise exceptions.InvalidHost()
        except aiohttp.client_exceptions.ClientConnectorError:
            raise exceptions.ConnectError() from aiohttp.client_exceptions.ClientConnectorError
        except aiohttp.client_exceptions.ServerDisconnectedError:
            pass

    async def send_post(self):
        """Send post request."""
        try:
            async with timeout(TIMEOUT, loop=self._loop):
                request = self._session.post(
                    "http://" + self.host + self.endpoint,
                    json=self.payload,
                    headers=HEADER,
                    verify=False,
                )
                self.data = await request.json()
        except aiohttp.client_exceptions.ClientConnectorError:
            raise exceptions.ConnectError() from aiohttp.client_exceptions.ClientConnectorError
        except aiohttp.client_exceptions.ServerDisconnectedError:
            pass

    def status(self):
        """Return the status of the Yeti."""
        return self.data
