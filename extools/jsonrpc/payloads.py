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
