"""Exceptions for Goal Zero Yeti API Python client"""


class ConnectError(Exception):
    """When a connection error is encountered."""


class InvalidHost(Exception):
    """The URL provided was somehow invalid."""

