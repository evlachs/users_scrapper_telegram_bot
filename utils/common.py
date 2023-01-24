import inspect
import textwrap
from typing import Any

DEF_LEN = 111


def shortext(s: Any, len=DEF_LEN) -> str: return textwrap.shorten(str(s), width=len)


def current_function():
    return inspect.currentframe().f_code.co_name


def caller_function():
    caller_frame = inspect.currentframe().f_back
    return caller_frame.f_code.co_name


__all__ = [g for g in globals() if g[0] != '_']
