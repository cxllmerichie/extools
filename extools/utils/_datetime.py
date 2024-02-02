from datetime import datetime, timezone

from ..types import PreciseUnixUtc


def unixnow() -> PreciseUnixUtc:
    return datetime.timestamp(datetime.now())


def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc).replace(second=0, microsecond=0, tzinfo=None)


def isonow() -> str:
    return datetime.utcnow().isoformat()
