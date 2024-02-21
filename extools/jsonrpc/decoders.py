from .. import utils
from . import _types


def to_str(
        hex: _types.HexStr,  # noqa
) -> str:
    stripped = hex[66:]
    length = int(stripped[:64], 16) * 2
    hex = stripped[64: 64 + length]
    return bytes.fromhex(hex).decode().rstrip('\x00')


def to_int(
        hex: _types.HexStr,  # noqa
) -> int:
    return int(hex, 16)


def to_addr(
        hex: _types.HexStr,  # noqa
) -> str:
    return str(utils.to_checksum_address(hex[:2] + hex[26:]))
