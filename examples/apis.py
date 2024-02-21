from extools import apis

import asyncio


async def main():
    # async with apis.CryptoAPI() as api:
    #     response = await api(endpoint=f'/chain/1')
    #     print(response)

    # async with apis.DexTools(key='uIWQjThsvQ7PWc0oKWFtm2VEJSMdThME3cLZNUqZ') as api:
    #     response = await api(endpoint=f'/token/alvey/0xCb3e9919C56efF1004E54175a01e39163a352129/price')
    #     print(response)

    async with apis.CoinGecko() as api:
        response = await api(endpoint=f'/simple/token_price/alvey-chain', params=dict(
            contract_addresses='0xCb3e9919C56efF1004E54175a01e39163a352129',
            vs_currencies='usd',
        ))
        print(response)

    # async with apis.GeckoTerminal() as api:
    #     response = await api(endpoint=f'/simple/networks/eth/token_price/0x256D1fCE1b1221e8398f65F9B36033CE50B2D497')
    #     print(response)

    # async with apis.DexScreener() as api:
    #     response = await api(endpoint=f'/tokens/0xCb3e9919C56efF1004E54175a01e39163a352129')
    #     print(response)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
