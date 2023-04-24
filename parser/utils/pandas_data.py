"""
Contains methods for pandas data processing
"""
from typing import Any, Optional

import pandas as pd
from tqdm.asyncio import trange

from .metric_type import MetricType


def combine_metric_data(
    companies: list[tuple[int, str]],
    metrics: dict,
    metric_type: MetricType,
    year: int,
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


async def write_excel_data(
    file_name: str,
    start_year: int,
    end_year: int,
    companies_metrics: dict,
    companies: Optional[list[str]] = None,
    functor_get_top_companies: Any = None,
) -> None:
    with pd.ExcelWriter(file_name) as writer:
        async for year in trange(
            start_year,
            end_year + 1,
            desc='Download companies by year',
        ):
            yearly_companies_data = {}

            for metric, company_metric in companies_metrics.items():
                if (companies is None) or (functor_get_top_companies is None):
                    companies = [
                        (i, company) for i, company in enumerate(company_metric.keys())
                    ]
                else:
                    companies = await functor_get_top_companies(
                        year, companies=companies,
                    )

                metric_data = combine_metric_data(
                    companies=companies,
                    metrics=company_metric,
                    metric_type=metric,
                    year=year,
                )

                if len(yearly_companies_data) == 0:
                    yearly_companies_data = metric_data
                else:
                    for company, _ in yearly_companies_data.items():
                        if company in metric_data:
                            yearly_companies_data[company] |= metric_data[company]
            pd.DataFrame.from_dict(yearly_companies_data, orient='index').to_excel(
                writer,
                sheet_name=str(year),
            )
    print(f'Successfully saved data in {file_name}!')
