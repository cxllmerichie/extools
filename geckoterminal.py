from typing import Any, Optional
import ujson as json
import asyncio
import aiohttp

from .utils import unixnow
from . import logman, types


class API:
    fetched_at: float = unixnow()
    delay_sec: int = 0.5  # 30 requests per minute

    def __init__(self, logger: logman.Logger):
        self.logger: logman.Logger = logger

    async def __call__(self, endpoint: str, params: dict[str, Any] = None) -> Optional[types.JSONResponse]:
        try:
            async with aiohttp.ClientSession(
                    base_url='https://api.geckoterminal.com',
                    json_serialize=json.dumps,
            ) as session:
                async with session.get(
                        url=f'/api/v2/{endpoint}',
                        params=json.dumps(params) if params else None,
                        headers={
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
