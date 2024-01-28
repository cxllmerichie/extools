from typing import Any, Optional
import asyncio
import aiohttp

from . import logman, types, json
from .utils import unixnow


class API:
    fetched_at: float = unixnow()
    delay_sec: int = 0.66  # 40 requests per minute

    def __init__(self, key: str, logger: logman.Logger):
        self.key: str = key
        self.logger: logman.Logger = logger

    async def __call__(self, endpoint: str, params: dict[str, Any] = None) -> Optional[types.JSONResponse]:
        try:
            async with aiohttp.ClientSession(
                    base_url='https://open-api.dextools.io',
                    json_serialize=json.dumps,
            ) as session:
                async with session.get(
                        url=f'/free/v2/{endpoint}',
                        params=params,
                        headers={
                            'X-BLOBR-KEY': self.key,
                            'accept': 'application/json',
                        },
                ) as r:
                    return await r.json()
        except Exception as e:
            self.logger.error(e)

    async def __aenter__(self):
        passed_sec = unixnow() - API.fetched_at
        if passed_sec < API.delay_sec:
            await asyncio.sleep(API.delay_sec - passed_sec)
        API.fetched_at = unixnow()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...
