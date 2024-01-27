import orjson as json
import aiohttp

from . import types


async def request(
        url: str,
        payload: list[tuple[types.Payload, dict[types.CallID, types.Decoder]]],
) -> list[types.DecodedResponse]:
    decoders: dict[types.CallID, types.Decoder] = {tuple(d[1].keys())[0]: tuple(d[1].values())[0] for d in payload}
    try:
        async with aiohttp.ClientSession(
                json_serialize=json.dumps,
        ) as s:
            async with s.post(
                    url=url,
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps([p[0] for p in payload]),
            ) as r:
                return [decoders[response['id']](response['result']) for response in await r.json()]
    except Exception as e:
        print(e)
        return []
