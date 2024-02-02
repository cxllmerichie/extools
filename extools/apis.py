from abc import ABC, abstractmethod
from typing import Any, Optional
import asyncio
import aiohttp

from . import logman, types, json, utils


class Limiter(ABC):
    fetched_at: float = utils.unixnow()
    delay_sec: float = 0  # 60 / req_per_min

    def __init__(self, logger: Optional[logman.Logger]):
        self.logger: Optional[logman.Logger] = logger

    @abstractmethod
    async def __call__(self, endpoint: str, params: dict[str, Any] = None) -> Optional[types.JSONResponse]:
        ...

    async def request(
            self,
            url: types.URL,
            endpoint: str,
            params: dict[str, Any] = None,
            headers: dict[str, Any] = None,
    ) -> Optional[types.JSONResponse]:
        try:
            async with aiohttp.ClientSession(
                    base_url=url,
                    json_serialize=json.dumps,
            ) as session:
                async with session.get(
                        url=endpoint,
                        params=json.dumps(params) if params else None,
                        headers=headers,
                ) as r:
                    return await r.json()
        except Exception as e:
            if self.logger:
                self.logger.error(e)

    async def __aenter__(self):
        passed_sec = utils.unixnow() - Limiter.fetched_at
        if passed_sec < Limiter.delay_sec:
            await asyncio.sleep(Limiter.delay_sec - passed_sec)
        Limiter.fetched_at = utils.unixnow()
        return self

    async def __aexit__(self, _, __, ___):
        ...


class DexTools(Limiter):
    delay_sec: int = 60 / 40

    def __init__(self, key: str, logger: logman.Logger):
        self.key: str = key
        super().__init__(logger=logger)

    async def __call__(self, endpoint: str, params: dict[str, Any] = None) -> Optional[types.JSONResponse]:
        return await super().request(
            url='https://open-api.dextools.io',
            endpoint=f'/free/v2/{endpoint}',
            params=params,
            headers={'X-BLOBR-KEY': self.key, 'accept': 'application/json'},
        )


class DexScreener(Limiter):
    delay_sec: int = 60 / 300

    async def __call__(self, endpoint: str, params: dict[str, Any] = None) -> Optional[types.JSONResponse]:
        return await super().request(
            url='https://api.dexscreener.com',
            endpoint=f'/latest/dex/{endpoint}',
            params=params,
            headers={'accept': 'application/json'},
        )


class GeckoTerminal(Limiter):
    delay_sec: int = 60 / 30

    async def __call__(self, endpoint: str, params: dict[str, Any] = None) -> Optional[types.JSONResponse]:
        return await super().request(
            url='https://api.geckoterminal.com',
            endpoint=f'/api/v2/{endpoint}',
            params=params,
            headers={'accept': 'application/json'},
        )


class CoinGecko(Limiter):
    delay_sec: int = 60 / 30

    async def __call__(self, endpoint: str, params: dict[str, Any] = None) -> Optional[types.JSONResponse]:
        return await super().request(
            url='https://api.coingecko.com',
            endpoint=f'/api/v3/{endpoint}',
            params=params,
            headers={'accept': 'application/json'},
        )


class CryptoAPI(Limiter):
    async def __call__(self, endpoint: str, params: dict[str, Any] = None) -> Optional[types.JSONResponse]:
        return await super().request(
            url='http://127.0.0.1:9876',
            endpoint=endpoint,
            params=params,
            headers={'accept': 'application/json'},
        )

    async def __aenter__(self):
        return self
