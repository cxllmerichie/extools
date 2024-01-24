from web3 import types
import web3


def hex_to_str(
        hex: types.HexStr,
) -> str:
    stripped = hex[66:]
    length = int(stripped[:64], 16) * 2
    hex = stripped[64: 64 + length]
    return bytes.fromhex(hex).decode('utf-8').rstrip('\x00')


def hex_to_int(
        hex: types.HexStr,
) -> int:
    return int(hex, 16)


def hex_to_addr(
        hex: types.HexStr,
) -> str:
    return str(web3.Web3.to_checksum_address(hex[:2] + hex[26:]))
