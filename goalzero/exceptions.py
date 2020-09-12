"""Exceptions for Goal Zero Yeti API Python client"""


class RequestException(IOError):
    """There was an ambiguous exception that occurred while handling your
    request.
    """

    def __init__(self, *args, **kwargs):
        """Initialize RequestException with `request` and `response` objects."""
        response = kwargs.pop("response", None)
        self.response = response
        self.request = kwargs.pop("request", None)
        if response is not None and not self.request and hasattr(response, "request"):
            self.request = self.response.request
        super().__init__(*args, **kwargs)


class ConnectError(Exception):
    """When a connection error is encountered."""
    
    pass


class ConnectTimeout(ConnectError):
    """The request timed out while trying to connect to the remote server."""
    
    pass


class HostRequired(RequestException):
    """When a host is not provided."""
    
    pass


class InvalidHost(RequestException):
    """The URL provided was somehow invalid."""
    
    pass

