from typing import Optional, Any, Union, AsyncGenerator
from aioredis import Redis as _Redis
from contextlib import suppress
import ujson as json

from . import types


class Redis(_Redis):
    async def clear(self) -> None:
        async for key in self.scan_iter():
            await self.delete(key)


class RedisLookup(Redis):  # TODO: speedup
    async def findkey(self, **kwargs: Any) -> Optional[str]:
        async for key in self.findkeys(**kwargs):
            return key

    async def findkeys(self, **kwargs: Any) -> AsyncGenerator[str, None]:
        for k, v in kwargs.items():
            async for key in self.scan_iter(match=f'*:{k}:{v}:*'):
                yield key

    async def findone(self, **kwargs: Any) -> Optional[Any]:
        async for value in self.findall(**kwargs):
            return value

    async def findall(self, **kwargs: Any) -> AsyncGenerator[Any, None]:
        async for key in self.findkeys(**kwargs):
            yield await self.get(key)

    @staticmethod
    def extract(key: str, what: str) -> Optional[str]:
        data: list[str] = key.split(':')
        return data[data.index(what) + 1]


class RedisJSON(RedisLookup):
    # override
    async def get(self, name: str) -> Optional[types.AttrDict[str, Any]]:
        if value := await super().get(name):
            if isinstance(value, str):
                with suppress(Exception):
                    return types.AttrDict(json.loads(value))
            return value

    # override
    async def set(self, name: str, value: Union[str, dict[Any, Any]], *args):
        if isinstance(value, dict):
            value = json.dumps(value)
        return await super().set(name, value, *args)