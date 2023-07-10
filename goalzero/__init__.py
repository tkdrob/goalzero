"""
Goal Zero Rest Api
~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2020 by Robert Hillis.
Not affiliated with Goal Zero. Credit for headers belongs to Goal Zero.
:license: Apache 2.0, see LICENSE for more details.
"""
import asyncio
import aiohttp

from . import exceptions

HEADER = {
    "Content-Type": "application/json",
    "User-Agent": "YetiApp/1340 CFNetwork/1125.2 Darwin/19.4.0",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "Accept-Language": "en-us",
    "Accept-Encoding": "gzip, deflate",
    "Cache-Control": "no-cache",
}
TIMEOUT = 10

semaphore = asyncio.Semaphore()


class Yeti:
    """A class for handling connections with a Goal Zero Yeti."""

    def __init__(self, host: str, session: aiohttp.ClientSession, **data) -> None:
        """Initialize the connection to Goal Zero Yeti instance."""
        self._session = session
        self.control = {}
        self.data = {}
        self.endpoint = {}
        self.host = host
        self.payload = {}
        self.mac = None
        self.sysdata = {}

    async def init_connect(self) -> None:
        """Get states from Goal Zero Yeti instance."""
        self.endpoint = "/sysinfo"
        self.control = "name"
        await Yeti.send_get(self)
        self.control = "thingName"
        self.endpoint = "/state"
        await Yeti.send_get(self)

    async def get_state(self) -> None:
        """Get states from Goal Zero Yeti instance."""
        self.control = "thingName"
        self.endpoint = "/state"
        await Yeti.send_get(self)

    async def post_state(self, payload) -> None:
        """Post payload to Goal Zero Yeti instance."""
        self.endpoint = "/state"
        self.payload = payload
        await Yeti.send_post(self)

    async def sysinfo(self) -> None:
        """Get system info from Goal Zero Yeti instance."""
        self.endpoint = "/sysinfo"
        self.control = "name"
        await Yeti.send_get(self)

    async def reset(self) -> None:
        """Reset Goal Zero Yeti instance."""
        self.endpoint = "/factory-reset"
        await Yeti.send_get(self)

    async def reboot(self) -> None:
        """Reboot Goal Zero Yeti instance."""
        self.endpoint = "/rpc/Sys.Reboot"
        await Yeti.send_get(self)

    async def get_loglevel(self) -> None:
        """Get log level Goal Zero Yeti instance."""
        self.endpoint = "/loglevel"
        self.control = "app"
        await Yeti.send_get(self)

    async def post_loglevel(self, payload) -> None:
        """Post log level Goal Zero Yeti instance."""
        self.endpoint = "/loglevel"
        self.payload = payload
        await Yeti.send_post(self)

    async def join(self, payload) -> None:
        """Join Goal Zero Yeti instance to Wifi network."""
        self.endpoint = "/join"
        self.payload = payload
        await Yeti.send_post(self)

    async def wifi(self) -> None:
        """Get available Wifi networks visible to Goal Zero Yeti instance."""
        self.endpoint = "/wifi"
        await Yeti.send_get(self)

    async def password_set(self, payload) -> None:
        """Set password to Zero Yeti instance."""
        self.payload = {"new_password": "" + payload + ""}
        self.endpoint = "/password-set"
        await Yeti.send_post(self)

    async def join_direct(self) -> None:
        """Directly Join Goal Zero Yeti instance on its Wifi."""
        self.endpoint = "/join-direct"
        await Yeti.send_post(self)

    async def start_pair(self) -> None:
        """Pair with Goal Zero Yeti instance."""
        self.endpoint = "/start-pair"
        await Yeti.send_post(self)

    async def send_get(self) -> None:
        """Send get request."""
        try:
            async with semaphore:
                response = await self._session.get(
                    url=f"http://{self.host}{self.endpoint}",
                    timeout=aiohttp.ClientTimeout(TIMEOUT),
                )
                if self.endpoint == "/sysinfo":
                    self.sysdata = await response.json()
                else:
                    self.data = await response.json()
                    if self.control not in self.data.keys():
                        raise exceptions.InvalidHost()
                    if self.data["socPercent"] > 100:
                        self.data["socPercent"] = 100
        except (
            OSError,
            TypeError,
            aiohttp.client_exceptions.ClientConnectorError,
            asyncio.exceptions.TimeoutError,
        ) as err:
            raise exceptions.ConnectError() from err
        except aiohttp.client_exceptions.ServerDisconnectedError:
            pass

    async def send_post(self) -> None:
        """Send post request."""
        try:
            async with semaphore:
                request = await self._session.post(
                    url=f"http://{self.host}{self.endpoint}",
                    json=self.payload,
                    headers=HEADER,
                    timeout=aiohttp.ClientTimeout(TIMEOUT),
                )
                self.data = await request.json()
                if self.data["socPercent"] > 100:
                    self.data["socPercent"] = 100
        except (
            OSError,
            TypeError,
            aiohttp.client_exceptions.ClientConnectorError,
            asyncio.exceptions.TimeoutError,
        ) as err:
            raise exceptions.ConnectError() from err
        except aiohttp.client_exceptions.ServerDisconnectedError:
            pass
