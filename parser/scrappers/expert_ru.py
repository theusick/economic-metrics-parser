import logging
import re
from parser.config import config
from parser.scrappers.base_scrapper import BaseScrapper
from parser.utils import convert_company_name
from typing import Union

from bs4 import BeautifulSoup, NavigableString, Tag


log = logging.getLogger(__name__)


class ExpertScrapper(BaseScrapper):
    """
    Scrapper for Expert site.
    """

    def __init__(self) -> None:
        super().__init__()
        self.base_url = config.COMPANIES_BASE_URL

    async def scrap(self, upload_year: int) -> list[tuple[int, str]]:
        """
        Get companies name by year.
        """
        log.debug('Start scrapping expert by upload_year=%s', upload_year)

        companies = []
        if (
            upload_year is None
            or upload_year < config.METRICS_POSSIBLE_START_YEAR
            or upload_year > config.METRICS_POSSIBLE_END_YEAR
        ):
            return companies
        # Get a list of the TOP companies rated "Expert" in `METRICS_YEAR` year
        companies_table = await self.__get_companies_table(
            url=self.base_url + '/' + str(upload_year),
        )
        companies_rows = companies_table.find_all('tr')
        for row in companies_rows[1 : len(companies_rows)]:
            cells = row.find_all('td')
            if len(cells):
                company_top_pos = self.__convert_top_number(cells[0].text)
                company_name = convert_company_name(cells[1].text)

                companies.append((company_top_pos, company_name))
        return companies

    def __convert_top_number(self, row_top_number: str) -> str:
        result = re.search(r'\d+', row_top_number)
        if result:
            result = result.group()
        else:
            result = '-'
        return result

    async def __get_companies_table(
        self,
        url: str,
    ) -> Union[Tag, NavigableString, None]:
        async with self._session.get(url) as response:
            text = await response.read()
            main_soup = BeautifulSoup(text.decode('utf-8'), 'lxml')
            return main_soup.find('table', class_='rating-table')
