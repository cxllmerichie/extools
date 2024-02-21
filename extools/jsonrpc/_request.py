from typing import Any
import aiohttp

from . import _types
from .. import json


async def request(
        url: str,
        payload: dict[str, dict[str, Any]],
) -> tuple[_types.DecodedResponse, ...]:
    async with aiohttp.ClientSession(
            json_serialize=json.dumps,
    ) as s:
        async with s.post(
                url=url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps([value['payload'] for value in payload.values()]),
        ) as r:
            return tuple(
                payload[response['id']]['decoder'](response['result'])
                for response in await r.json()
            )
