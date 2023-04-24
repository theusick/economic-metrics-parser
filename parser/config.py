"""
Main config of the app
"""

from enum import Enum
from parser.utils import MetricType


class ParserMode(Enum):
    # Download first top-400 companies, then past metrics by them
    TOP_400 = 'top-400'
    # Download only default metrics
    DIVIDENDS = 'dividends'
    # Download metrics for `РСБУ`
    RAS = 'ras'

    def __str__(self):
        return self.value


class Config:
    """
    Class for storing static const values
    """

    CLIENT_HEADERS = {
        'Accept': 'text/html',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    }

    COMPANIES_BASE_URL = 'https://expert.ru/expert400'

    METRICS_BASE_URL = 'https://smart-lab.ru/q/shares_fundamental4'
    DIVIDENDS_METRICS_WITH_FILTER = [
        MetricType('Выручка', 'revenue'),
        MetricType('Прибыль', 'net_income'),
        MetricType('Дивиденд на АО', 'dividend'),
        MetricType('Дивиденд на ПА', 'dividend_pr'),
        MetricType('Выплата дивидендов', 'dividend_payout'),
    ]

    RAS_URL_MIXIN = '&type=RSBU'

    RAS_METRICS_WITH_FILTER = DIVIDENDS_METRICS_WITH_FILTER.copy()
    RAS_METRICS_WITH_FILTER.extend(
        [
            MetricType('Рентабельность Капитала Roe', 'roe'),
            MetricType('Рентабельность Активов Roa', 'roa'),
            MetricType('Общий Долг', 'debt'),
            MetricType('Мультипликатор P/Bv (Цена/Балансовая Стоимость)', 'p_bv'),
            MetricType('Число Акций Ао', 'number_of_shares'),
            MetricType('Число Акций Ао', 'number_of_priv_shares'),
        ],
    )
    METRICS_POSSIBLE_START_YEAR = 2013
    METRICS_POSSIBLE_END_YEAR = 2022

    OUTPUT_DEFAULT_FILE = 'output.xlsx'


config = Config()
