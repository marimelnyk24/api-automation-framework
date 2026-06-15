from contextvars import ContextVar


_last_response = ContextVar(
    "last_response",
    default=None
)


def set_last_response(response):
    _last_response.set(response)


def get_last_response():
    return _last_response.get()