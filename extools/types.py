from __future__ import annotations

from typing import Type, TypeVar, Union, Iterable, Any, NewType
from pydantic import GetCoreSchemaHandler
from web3 import Web3, types as w3types
from pydantic import JsonValue, HttpUrl
from pydantic_core import core_schema

from web3.types import (
    BlockNumber,
)


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


class HexStr(str):
    @classmethod
    def process(cls, address: Union[str, w3types.HexBytes]) -> str:
        if isinstance(address, w3types.HexBytes):
            address = address.hex()
        return address

    @classmethod
    def __get_pydantic_core_schema__(
            cls, _: Type[Any], __: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            function=cls.process,
            schema=core_schema.str_schema(),
        )


class Address(HexStr):
    @classmethod
    def process(cls, address: Union[str, w3types.HexBytes]) -> str:
        address = super(Address, cls).process(address)
        if len(address) != 42:
            address = address[:2] + address[26:]
        if len(address) != 42:
            raise ValueError('Any `Address` length must be 42')
        return str(Web3.to_checksum_address(address))

    def __new__(cls, *args, **kwargs):
        return cls.process(args[0])


class ContractAddress(Address):
    ...


class PairAddress(ContractAddress):
    ...


class WalletAddress(Address):
    ...


class Hash(HexStr):
    @classmethod
    def process(cls, hash: Union[str, w3types.HexBytes]) -> str:
        hash = super(Hash, cls).process(hash)
        if len(hash) != 66:
            raise ValueError('Any `Hash` length must be 66')
        return hash

    def __new__(cls, *args, **kwargs):
        return cls.process(args[0])


class TxHash(Hash):
    ...


class BlockHash(Hash):
    ...


BlockIdentifier: Type = Union[BlockNumber, BlockHash]
NetworkID: Type = NewType('NetworkID', int)

PreciseUnixUtc: Type = NewType('PreciseUnixUtc', float)
ImpreciseUnixUtc: Type = NewType('ImpreciseUnixUtc', int)
HTML: Type = NewType('HTML', str)

JSONResponse: Type = JsonValue
URL: Type = HttpUrl
