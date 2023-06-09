import logging
from parser.config import config
from parser.scrappers.base_scrapper import BaseScrapper
from parser.utils import MetricType
from typing import Union

from bs4 import BeautifulSoup, NavigableString, Tag


log = logging.getLogger(__name__)


class SmartLabScrapper(BaseScrapper):
    """
    Scrapper for smart-lab site
    """

    def __init__(self) -> None:
        super().__init__()
        self.base_url = config.METRICS_BASE_URL

    async def scrap(self, metric: MetricType, **kwargs) -> dict:
        """
        Get companies economic table by metric type
        """
        log.debug(
            'Start scrapping smart_lab_ru by metric.name=%s, metric.filter=%s',
            metric.name,
            metric.filter,
        )

        companies_name = kwargs.get('companies', None)
        url_mixin = kwargs.get('url_mixin', '')

        companies_metrics = {}

        if (metric is None) or (not isinstance(metric, MetricType)):
            return companies_metrics

        metrics_table = await self.__get_companies_metrics_table(
            url=self.base_url + '/?field=' + metric.filter + url_mixin,
        )
        table_years = self.__parse_table_years(metrics_table)

        metrics_rows = metrics_table.find_all('tr')
        for row in metrics_rows:
            columns = row.find_all('td')
            if len(columns) < 3:
                continue

            company_name = self.convert_company_name(columns[1].find('a').text)
            if companies_name is not None:
                company_name = self._find_company_name(companies_name, company_name)

            years_data, table_row_offset = {}, len(columns) - len(table_years) - 2
            # Skip the last column, since there is a percentage ratio
            for i, col in enumerate(columns[table_row_offset : len(columns) - 2]):
                column_value = col.text.strip().replace(' ', '')
                if len(column_value) == 0:
                    column_value = 0
                years_data[table_years[i]] = column_value

            companies_metrics[company_name] = years_data
        return companies_metrics

    def __parse_table_years(self, metrics_table) -> list[int]:
        years = []

        table_years_elements = metrics_table.find('tr').select('th a')
        for element in table_years_elements:
            year = element.text.strip()
            if year.isnumeric():
                years.append(year)
        return years

    async def __get_companies_metrics_table(
        self,
        url: str,
    ) -> Union[Tag, NavigableString, None]:
        async with self._session.get(url, headers=config.CLIENT_HEADERS) as response:
            text = await response.read()
            main_soup = BeautifulSoup(text.decode('utf-8'), 'lxml')
            return main_soup.find('table', class_='simple-little-table')
