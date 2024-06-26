from typing import Callable, Any, NewType, TypedDict


HexStr = NewType("HexStr", str)

CallMethod = str
CallID = str
DecodedResponse = Any
Decoder = Callable[[HexStr], DecodedResponse]
CallParams = list[Any]
Payload = dict[str, Any]

CallData = TypedDict('CallData', {
    'decoder': Decoder,
    'params': CallParams,
    'method': CallMethod,
})
