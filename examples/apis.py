from extools import apis
import aiohttp

import asyncio


async def main():
    async with apis.CryptoAPI() as api:
        response = await api(endpoint=f'/chain/1')
        print(response)

    async with apis.DexTools(key='uIWQjThsvQ7PWc0oKWFtm2VEJSMdThME3cLZNUqZ') as api:
        response = await api(endpoint=f'/token/alvey/0xa0C0e4A09715E7B8e03aDeB5699628B7aE3ed8eD/price')
        print(response)

    async with apis.CoinGecko() as api:
        response = await api(endpoint=f'/simple/token_price/ethereum', params=dict(
            contract_addresses='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
            vs_currencies='usd',
        ))
        print(response)

    async with apis.GeckoTerminal() as api:
        response = await api(endpoint=f'/search/pools', params=dict(
            query='ETH',
            network='eth',
            page=1,
        ))
        print(response)

    async with apis.DexScreener() as api:  # FIXME
        response = await api(endpoint=f'/tokens/0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
        print(response)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
