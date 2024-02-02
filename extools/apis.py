from typing import Optional
import asyncio as _asyncio
import aiohttp as _aiohttp
import abc as _abc

from . import logman, types, json, utils as _utils


class _API(_abc.ABC):
    def __init__(self, logger: Optional[logman.Logger] = None):
        self.logger: Optional[logman.Logger] = logger

    @_abc.abstractmethod
    async def __call__(self, endpoint: str, **kwargs) -> Optional[types.JSONResponse]:
        ...

    async def __aenter__(self):
        return self

    async def __aexit__(self, _, __, ___):
        ...

    async def request(
            self,
            url: types.URL,
            endpoint: str,
            **kwargs,
    ) -> Optional[types.JSONResponse]:
        kwargs['headers'] = kwargs.get('headers', dict()) | {'accept': 'application/json'}
        try:
            async with _aiohttp.ClientSession(
                    base_url=url,
                    json_serialize=json.dumps,
            ) as session:
                async with session.get(
                        url=endpoint,
                        **kwargs,
                ) as r:
                    return await r.json()
        except Exception as e:
            if self.logger:
                self.logger.error(e)


class _RateLimitedAPI(_API, _abc.ABC):
    _fetched_at: float = float('-inf')

    @property
    @_abc.abstractmethod
    def rate(self) -> int:
        """
        Max requests per 60 sec.
        :return:
        """

    # async def __aenter__(self):
    #     passed_sec = _utils.unixnow() - self.__class__._fetched_at
    #     delay_sec = 60 / self.rate
    #
    #     if passed_sec < delay_sec:
    #         await _asyncio.sleep(delay_sec - passed_sec)
    #     self.__class__._fetched_at = _utils.unixnow()
    #
    #     return self


class DexTools(_RateLimitedAPI):
    @property
    def rate(self):
        return 120

    def __init__(self, key: str, logger: Optional[logman.Logger] = None):
        self.key: str = key
        super().__init__(logger=logger)

    async def __call__(self, endpoint: str, **kwargs) -> Optional[types.JSONResponse]:
        return await super().request(  # no `json.dumps(params)`
            url='https://public-api.dextools.io',
            endpoint=f'/standard/v2{endpoint}',
            headers={'X-API-Key': self.key},
            **kwargs,
        )


class DexScreener(_RateLimitedAPI):
    @property
    def rate(self):
        return 300

    async def __call__(self, endpoint: str, **kwargs) -> Optional[types.JSONResponse]:
        return await super().request(
            url='https://api.dexscreener.com',
            endpoint=f'/latest/dex{endpoint}',
            **kwargs,
        )


class GeckoTerminal(_RateLimitedAPI):
    @property
    def rate(self):
        return 30

    async def __call__(self, endpoint: str, **kwargs) -> Optional[types.JSONResponse]:
        return await super().request(
            url='https://api.geckoterminal.com',
            endpoint=f'/api/v2{endpoint}',
            **kwargs,
        )


class CoinGecko(_RateLimitedAPI):
    @property
    def rate(self):
        return 30

    async def __call__(self, endpoint: str, **kwargs) -> Optional[types.JSONResponse]:
        return await super().request(
            url='https://api.coingecko.com',
            endpoint=f'/api/v3{endpoint}',
            **kwargs,
        )


class CryptoAPI(_API):
    async def __call__(self, endpoint: str, **kwargs) -> Optional[types.JSONResponse]:
        return await super().request(
            url='http://127.0.0.1:9876',
            endpoint=endpoint,
            **kwargs,
        )
