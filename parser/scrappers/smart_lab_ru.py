import logging

from typing import Union
from bs4 import BeautifulSoup, Tag, NavigableString, ResultSet

from parser.config import config
from parser.scrappers.base_scrapper import BaseScrapper
from parser.utils import MetricType, convert_company_name

log = logging.getLogger(__name__)


class SmartLabScrapper(BaseScrapper):
    """
    Scrapper for smart-lab site.
    """

    def __init__(self) -> None:
        super().__init__()
        self.base_url = config.METRICS_BASE_URL

    async def scrap(self, metric: MetricType, **kwargs) -> dict:
        """
        Get companies economic table by metric type.
        """
        log.debug(f"Start scrapping smart_lab_ru by metric={metric.name}")

        companies_name = kwargs.get("companies", None)

        companies_metrics = {}

        if (metric is None) or (metric not in config.METRICS_WITH_FILTER):
            return companies_metrics

        metrics_table = await self.__get_companies_metrics_table(
            url=self.base_url + "/?field=" + metric.filter
        )
        table_years = self.__parse_table_years(metrics_table)

        metrics_rows = metrics_table.find_all("tr")
        for row in metrics_rows:
            columns = row.find_all("td")
            if len(columns) < 3:
                continue

            company_name = convert_company_name(columns[1].find("a").text)
            if len(companies_name) != 0:
                company_name = self.__find_company_name(companies_name, company_name)

            years_data, table_row_offset = {}, len(columns) - len(table_years) - 1
            # Skip the last column, since there is a percentage ratio
            for i, col in enumerate(columns[table_row_offset : len(columns) - 1]):
                column_value = col.text.strip().replace(" ", "")
                if len(column_value) == 0:
                    column_value = 0
                years_data[table_years[i]] = float(column_value)

            companies_metrics[company_name] = years_data
        return companies_metrics

    def __find_company_name(
        self, companies_name: list[str], substring_name: str
    ) -> str:
        for company_name in companies_name:
            if substring_name in company_name:
                return company_name
        return None

    def __parse_table_years(self, metrics_table) -> list[int]:
        years = []

        table_years_elements = metrics_table.find("tr").select("th a")
        for element in table_years_elements:
            year = element.text.strip()
            if year.isnumeric():
                years.append(year)
        return years

    async def __get_companies_metrics_table(
        self, url: str
    ) -> Union[Tag, NavigableString, None]:
        async with self._session.get(url) as response:
            text = await response.read()
            main_soup = BeautifulSoup(text.decode("utf-8"), "lxml")
            return main_soup.find("table", class_="simple-little-table")
