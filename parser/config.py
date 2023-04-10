"""
Main config of the app
"""

from parser.utils import MetricType


class Config:
    """
    Class for storing static const values
    """

    COMPANIES_BASE_URL = 'https://expert.ru/expert400'

    METRICS_BASE_URL = 'https://smart-lab.ru/q/shares_fundamental4'
    METRICS_WITH_FILTER = [
        MetricType('Выручка', 'revenue'),
        MetricType('Прибыль', 'net_income'),
        MetricType('Дивиденд на АО', 'dividend'),
        MetricType('Дивиденд на ПА', 'dividend_pr'),
        MetricType('Выплата дивидендов', 'dividend_payout'),
    ]
    METRICS_POSSIBLE_START_YEAR = 2013
    METRICS_POSSIBLE_END_YEAR = 2022

    OUTPUT_DEFAULT_FILE = 'output.xlsx'


config = Config()
