import asyncio

from extools import jsonrpc


async def main():
    response = await jsonrpc.request(url='https://eth-pokt.nodies.app', payload=(
            jsonrpc.payloads.block(hash='0x6142f8fe5e9f76cfae42e6959544af7bfc901de15abccdb8264b91e56c2c4bc2') |
            jsonrpc.payloads.block(hash='0x6142f8fe5e9f76cfae42e6959544af7bfc901de15abccdb8264b91e56c2c4bc2')
    ))
    print(response)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
