import aiohttp

from types import TracebackType
from typing import Optional, Type


class BaseScrapper:
    base_url: str

    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()

    async def __aenter__(self) -> "BaseScrapper":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._session.close()
