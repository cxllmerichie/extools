from typing_extensions import TypedDict
from typing import Callable
import uuid
import web3

from . import decoders, types


def payload(
        params: Callable[..., tuple[types.CallParams, types.Decoder, types.CallMethod]]
) -> Callable[..., tuple[types.Payload, dict[types.CallID, types.Decoder]]]:
    def wrapper(*args, **kwargs) -> tuple[types.Payload, dict[types.CallID, types.Decoder]]:
        call_id: types.CallID = str(uuid.uuid4())
        _params, decoder, method = params(*args, **kwargs)
        return {
            'jsonrpc': '2.0',
            'id': call_id,
            'method': method,
            'params': _params,
        }, {call_id: decoder}
    return wrapper


@payload
def token0(pair: str) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        {
            'to': web3.Web3.to_checksum_address(pair),
            'data': web3.Web3.keccak(text='token0()').hex(),
        },
        'latest'
    ], decoders.hex_to_addr, 'eth_call'


@payload
def token1(pair: str) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        {
            'to': web3.Web3.to_checksum_address(pair),
            'data': web3.Web3.keccak(text='token1()').hex(),
        },
        'latest'
    ], decoders.hex_to_addr, 'eth_call'


@payload
def symbol(contract: str) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        {
            'to': web3.Web3.to_checksum_address(contract),
            'data': web3.Web3.keccak(text='symbol()').hex(),
        },
        'latest'
    ], decoders.hex_to_str, 'eth_call'


@payload
def name(contract: str) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        {
            'to': web3.Web3.to_checksum_address(contract),
            'data': web3.Web3.keccak(text='name()').hex(),
        },
        'latest'
    ], decoders.hex_to_str, 'eth_call'


@payload
def get_reserves(pair: str) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    def decoder(reserves):
        reserves_bytes = bytes.fromhex(reserves[2:])
        reserves0 = int.from_bytes(reserves_bytes[:32], 'big')
        reserves1 = int.from_bytes(reserves_bytes[32: 64], 'big')
        return reserves0, reserves1

    return [
        {
            'to': web3.Web3.to_checksum_address(pair),
            'data': web3.Web3.keccak(text='getReserves()').hex(),
        },
        'latest'
    ], decoder, 'eth_call'


@payload
def decimals(contract: str) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        {
            'to': web3.Web3.to_checksum_address(contract),
            'data': web3.Web3.keccak(text='decimals()').hex(),
        },
        'latest'
    ], decoders.hex_to_int, 'eth_call'


@payload
def total_supply(contract: str) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        {
            'to': web3.Web3.to_checksum_address(contract),
            'data': web3.Web3.keccak(text='totalSupply()').hex(),
        },
        'latest'
    ], decoders.hex_to_int, 'eth_call'


@payload
def balance_of(contract: str, address: str) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        {
            'to': web3.Web3.to_checksum_address(contract),
            'data': f'0x70a08231000000000000000000000000{web3.Web3.to_checksum_address(address)[2:]}',
        },
        'latest'
    ], decoders.hex_to_int, 'eth_call'


@payload
def balance(address: str, identifier: int | str = 'latest') -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        web3.Web3.to_checksum_address(address),
        identifier,
    ], decoders.hex_to_int, 'eth_getBalance'


@payload
def receipt(txhash) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        txhash,
    ], lambda _: _, 'eth_getTransactionReceipt'


@payload
def block(hash: str, details: bool = False) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    """
    if isinstance(identifier, int) or identifier.lower() in {'latest', 'pending', 'earliest', 'safe', 'finalized'}:
        'eth_getBlockByNumber'
    else:
        'eth_getBlockByHash'
    :param hash:
    :param details:
    :return:
    """
    return [
        hash,
        details,
    ], lambda _: _, 'eth_getBlockByHash'


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
)) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        params,
    ], lambda _: _, 'eth_newFilter'


@payload
def entries(filter_id) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        filter_id,
    ], lambda _: _, 'eth_getFilterLogs'


@payload
def changes(filter_id) -> tuple[types.CallParams, types.Decoder, types.CallMethod]:
    return [
        filter_id,
    ], lambda _: _, 'eth_getFilterChanges'
