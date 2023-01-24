import functools
import logging as LOG


def _log_args_and_result(func):
    """
    A decorator that logs the input arguments and the result of the decorated function or method.
    #ChatGPT by created w/o changes
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


__all__ = [log, LOG]
