from typing import Callable, TypedDict, Any
import uuid
import web3

from . import decoders, _types
from .. import utils


def payload(
        call_data: Callable[..., _types.CallData]
) -> Callable[..., dict[str: dict[str, Any]]]:
    def wrapper(*args, **kwargs) -> dict[str: dict[str, Any]]:
        id, data = str(uuid.uuid4()), call_data(*args, **kwargs)
        return {id: {
            'payload': {
                'jsonrpc': '2.0',
                'id': id,
                'method': data['method'],
                'params': data['params'],
            },
            'decoder': data['decoder']
        }}

    return wrapper


@payload
def token0(pair: str) -> _types.CallData:
    return _types.CallData(
        method='eth_call',
        decoder=decoders.to_addr,
        params=[
            {
                'to': utils.to_checksum_address(pair),
                'data': web3.Web3.keccak(text='token0()').hex(),
            },
            'latest'
        ]
    )


@payload
def token1(pair: str) -> _types.CallData:
    return _types.CallData(
        method='eth_call',
        decoder=decoders.to_addr,
        params=[
            {
                'to': utils.to_checksum_address(pair),
                'data': web3.Web3.keccak(text='token1()').hex(),
            },
            'latest'
        ]
    )


@payload
def symbol(contract: str) -> _types.CallData:
    return _types.CallData(
        method='eth_call',
        decoder=decoders.to_str,
        params=[
            {
                'to': utils.to_checksum_address(contract),
                'data': web3.Web3.keccak(text='symbol()').hex(),
            },
            'latest'
        ]
    )


@payload
def name(contract: str) -> _types.CallData:
    return _types.CallData(
        method='eth_call',
        decoder=decoders.to_str,
        params=[
            {
                'to': utils.to_checksum_address(contract),
                'data': web3.Web3.keccak(text='name()').hex(),
            },
            'latest'
        ]
    )


@payload
def get_reserves(pair: str) -> _types.CallData:
    def decoder(reserves):
        reserves_bytes = bytes.fromhex(reserves[2:])
        reserves0 = int.from_bytes(reserves_bytes[:32], 'big')
        reserves1 = int.from_bytes(reserves_bytes[32: 64], 'big')
        return reserves0, reserves1

    return _types.CallData(
        method='eth_call',
        decoder=decoder,
        params=[
            {
                'to': utils.to_checksum_address(pair),
                'data': web3.Web3.keccak(text='getReserves()').hex(),
            },
            'latest'
        ]
    )


@payload
def decimals(contract: str) -> _types.CallData:
    return _types.CallData(
        method='eth_call',
        decoder=decoders.to_int,
        params=[
            {
                'to': utils.to_checksum_address(contract),
                'data': web3.Web3.keccak(text='decimals()').hex(),
            },
            'latest'
        ],
    )


@payload
def total_supply(contract: str) -> _types.CallData:
    return _types.CallData(
        method='eth_call',
        decoder=decoders.to_int,
        params=[
            {
                'to': utils.to_checksum_address(contract),
                'data': web3.Web3.keccak(text='totalSupply()').hex(),
            },
            'latest'
        ]
    )


@payload
def balance_of(contract: str, address: str) -> _types.CallData:
    return _types.CallData(
        method='eth_call',
        decoder=decoders.to_int,
        params=[
            {
                'to': utils.to_checksum_address(contract),
                'data': f'0x70a08231000000000000000000000000{utils.to_checksum_address(address)[2:]}',
            },
            'latest'
        ],
    )


@payload
def balance(address: str, identifier: int | str = 'latest') -> _types.CallData:
    return _types.CallData(
        method='eth_getBalance',
        decoder=decoders.to_int,
        params=[
            utils.to_checksum_address(address),
            identifier,
        ],
    )


@payload
def receipt(txhash) -> _types.CallData:
    return _types.CallData(
        method='eth_getTransactionReceipt',
        decoder=lambda _: _,
        params=[
            txhash
        ],
    )


@payload
def block(hash: str, details: bool = False) -> _types.CallData:
    """
    if isinstance(identifier, int) or identifier.lower() in {'latest', 'pending', 'earliest', 'safe', 'finalized'}:
        'eth_getBlockByNumber'
    else:
        'eth_getBlockByHash'
    :param hash:
    :param details:
    :return:
    """
    return _types.CallData(
        method='eth_getBlockByHash',
        decoder=lambda _: _,
        params=[
            hash,
            details,
        ],
    )


@payload
def filter(**params: TypedDict(
    'FilterParams', {
        'address': list,
        'blockHash': str,
        'fromBlock': str | int,
        'toBlock': str | int,
        'topics': list[str],
    },
    total=False
)) -> _types.CallData:
    return _types.CallData(
        method='eth_newFilter',
        decoder=lambda _: _,
        params=[
            params,
        ],
    )


@payload
def entries(filter_id) -> _types.CallData:
    return _types.CallData(
        method='eth_getFilterLogs',
        decoder=lambda _: _,
        params=[
            filter_id,
        ],
    )


@payload
def changes(filter_id) -> _types.CallData:
    return _types.CallData(
        method='eth_getFilterChanges',
        decoder=lambda _: _,
        params=[
            filter_id,
        ],
    )
