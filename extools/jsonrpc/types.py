from typing import Callable, Any
from web3 import types


CallMethod = str
CallID = str
DecodedResponse = Any
Decoder = Callable[[types.HexStr], DecodedResponse]
CallParams = list[Any]
Payload = dict[str, Any]
