from typing import Any
import orjson


def dumps(__obj, /) -> str:
    return orjson.dumps(__obj).decode()


def loads(__obj, /) -> Any:
    return orjson.loads(__obj)
