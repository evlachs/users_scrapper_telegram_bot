import functools
import logging, logging as LOG
from logging import root

import utils


class MyLogger(logging.Logger):
    """ Standard Logger wrapper """

    def exception(self, *a, **kw):
        msg, *a = a
        msg = msg or f"Some exception in {utils.caller_function()}"
        return super().exception(msg, *a, **kw)


def getMyLogger(name=None):
    """
    # getLogger() from logging.py ctrl+c ctrl_v -> for my logger using ability in style of usual Logger (by getLogger())
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    if not name or isinstance(name, str) and name == root.name:
        return root
    return MyLogger.manager.getLogger(name)


logger = getMyLogger()


# `? LOG=logger

def _log_args_and_result(func):
    """
    A decorator that logs the input arguments and the result of the decorated function or method.
    #ChatGPT by created w/o changes (almost))
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        LOG.debug(f'Calling {func.__name__} with args: {args}, kwargs: {kwargs}')
        result = func(*args, **kwargs)
        LOG.debug(f'{func.__name__} returned: {result}')
        return result

    return wrapper


def _log_info(*a, **kw):
    """ logger-info wrapper """
    msg, *a = a
    return LOG.info(msg, *a, **kw)


def log(*a, **kw):
    """ make `log` for simple using both for `log.ingo`- & calls-funcs- logging """
    return (
        _log_args_and_result
        if callable(a[0]) else
        _log_info
    )(*a, **kw)


__all__ = [log, LOG, logger]
