import textwrap
from typing import Any

DEF_LEN = 111


def shortext(s: Any, len=DEF_LEN) -> str: return textwrap.shorten(str(s), width=len)


__all__ = [g for g in globals() if g[0] != '_']
