"""
Abstract class for scrappers
"""

from abc import ABC
from types import TracebackType
from typing import Optional

import aiohttp


class BaseScrapper(ABC):
    """
    Abstract base scrapper class with async interface
    """

    base_url: str

    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()

    async def __aenter__(self) -> 'BaseScrapper':
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._session.close()

    def convert_company_name(self, row_company_name: str) -> str:
        return row_company_name.strip().replace('«', '').replace('»', '').lower()
