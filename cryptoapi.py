from typing import Any, Optional
import ujson as json
import aiohttp

from . import logman, types


class API:
    def __init__(self, logger: logman.Logger):
        self.logger: logman.Logger = logger

    async def __call__(self, endpoint: str, params: dict[str, Any] = None) -> Optional[types.JSONResponse]:
        try:
            async with aiohttp.ClientSession(
                    base_url='http://127.0.0.1:9876',
                    json_serialize=json.dumps,
            ) as session:
                async with session.get(
                        url=endpoint,
                        params=json.dumps(params) if params else None,
                        headers={
                            'accept': 'application/json',
                        },
                ) as r:
                    return await r.json()
        except Exception as e:
            self.logger.error(f'CryptoAPI: {await r.text()}, therefore {e}')

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...
