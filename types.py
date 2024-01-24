from __future__ import annotations

from typing import Type, TypeVar, Union, Iterable, Any
from web3 import Web3, types as w3types


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = AttrDict(v)

    def __dir__(self) -> Iterable[str]:
        return list(super().__dir__()) + [str(k) for k in self.keys()]

    def __getattr__(self, item: str) -> Any:
        if item in self:
            return self[item]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{item}'")

    def __getattribute__(self, item: str) -> Any:
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return self.__getattr__(item)

    def __setattr__(self, key: str, value: Any):
        self[key] = value


class Address(str):  # TODO: pydantic compatible
    def __new__(cls, *args, **kwargs):
        address: Union[str, w3types.HexBytes] = args[0]
        if isinstance(address, w3types.HexBytes):
            address = address.hex()
        if len(address) != 42:
            address = address[:2] + address[26:]
        return str(Web3.to_checksum_address(address))


class ContractAddress(Address):
    ...


class PairAddress(ContractAddress):
    ...


class WalletAddress(Address):
    ...


class Hash(str):
    def __new__(cls, *args, **kwargs):
        hash: Union[str, w3types.HexBytes] = args[0]
        if isinstance(hash, w3types.HexBytes):
            hash = hash.hex()
        return hash


class TxHash(Hash):
    ...


class BlockHash(Hash):
    ...


UnixTime: Type = TypeVar('UnixTime', bound=int)
HTML: Type = TypeVar('HTML', bound=str)
JSONItem = dict[str, Any]
JSONResponse = Union[JSONItem, list[JSONItem]]
