from typing import Callable, Any, Union
from web3 import types


CallMethod = str
CallID = str
DecodedResponse = Union[
    int,  # decimals, totalSupply, ...
    str,  # symbol, name, token0, token1, ...
    tuple[int, int],  # getReserves, ...
]
Decoder = Callable[[types.HexStr], DecodedResponse]
CallParams = list[Any]
Payload = dict[str, Any]
