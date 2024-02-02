from typing import AsyncGenerator, Any


async def aenumerate(
        iterable: AsyncGenerator[Any, None],
        start: int = 0
) -> AsyncGenerator[tuple[int, Any], None]:
    count: int = start
    async for element in iterable:
        yield count, element
        count += 1
