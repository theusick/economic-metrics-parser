import logging
import sys
from parser.utils import MetricType

import pandas as pd


if 'parser.config' not in sys.modules:
    from parser.config import config

log = logging.getLogger(__name__)


def combine_metric_data(
    companies: list[tuple[int, str]], metrics: dict, metric_type: MetricType, year: int,
) -> dict:
    result = {}

    for company in companies:
        company_data = {}

        company_name = company[1]
        company_data['N'] = company[0]

        if company_name in metrics:
            company_data[metric_type.name] = metrics[company_name][str(year)]
        result[company_name] = company_data
    return result


def create_metrics_dataframe(
    companies: list[tuple[int, str]], companies_metrics: dict, year: int,
):
    rows = []

    metric_columns = [metric_type.name for metric_type in config.METRICS_WITH_FILTER]

    for company in companies:
        name = company[1]
        if name in companies_metrics:
            if str(year) in companies_metrics[name]:
                revenue = companies_metrics[name][str(year)]
                profit = companies_metrics[name][str(year)]
                dividend_ao = companies_metrics[name][str(year)]
                dividend_pa = companies_metrics[name][str(year)]
                dividend_payment = companies_metrics[name][str(year)]
                rows.append(
                    [
                        company[0],
                        company[1],
                        revenue,
                        profit,
                        dividend_ao,
                        dividend_pa,
                        dividend_payment,
                    ],
                )
            else:
                rows.append([company[0], company[1], None, None, None, None, None])
        else:
            rows.append([company[0], company[1], None, None, None, None, None])

        dataframe = pd.DataFrame(rows, columns=metric_columns)

    return dataframe
