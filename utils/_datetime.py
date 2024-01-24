from datetime import datetime, timezone


def unixnow() -> float:
    return datetime.timestamp(datetime.now())


def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc).replace(second=0, microsecond=0, tzinfo=None)


def isonow() -> str:
    return datetime.utcnow().isoformat()
