import asyncio
import logging
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from parser.config import config
from parser.scrappers import ExpertScrapper, SmartLabScrapper
from parser.utils import MetricType, combine_metric_data

import pandas as pd
from aiomisc.log import LogFormat, LogLevel, basic_config
from tqdm.asyncio import trange


arg_parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

group = arg_parser.add_argument_group('Parser options')
group.add_argument(
    '-sy',
    '--start-year',
    type=int,
    default=2013,
    dest='metrics_start_year',
    help='Economic metrics upload start year. In range 2013-2022',
)

group.add_argument(
    '-ey',
    '--end-year',
    type=int,
    default=2021,
    dest='metrics_end_year',
    help='Economic metrics upload end year. In range 2013-2022',
)

group.add_argument(
    '-f',
    '--file',
    type=str,
    default=config.OUTPUT_DEFAULT_FILE,
    dest='output_file',
    help='Output file',
)

group = arg_parser.add_argument_group('Logging options')
group.add_argument(
    '-ll',
    '--log-level',
    type=str,
    default=LogLevel.default(),
    choices=LogLevel.choices(),
)
group.add_argument(
    '-lf',
    '--log-format',
    type=str,
    default=LogFormat.default(),
    choices=LogFormat.choices(),
)


log = logging.getLogger(__name__)


async def get_top_companies(upload_year: int, **kwargs) -> list[tuple[int, str]]:
    async with ExpertScrapper() as scrapper:
        companies = await scrapper.scrap(upload_year, **kwargs)
        return companies


async def get_companies_metrics(metric: MetricType, **kwargs):
    async with SmartLabScrapper() as scrapper:
        companies_metrics = await scrapper.scrap(metric, **kwargs)
        return companies_metrics


async def write_excel_top_400(
    file_name: str,
    start_year: int,
    end_year: int,
    companies_names: list,
    companies_metrics: dict,
) -> None:
    with pd.ExcelWriter(file_name) as writer:
        async for year in trange(
            start_year, end_year + 1, desc='Download companies by year',
        ):
            top_companies = await get_top_companies(year, companies=companies_names)

            yearly_companies_data = {}

            for metric, company_metric in companies_metrics.items():
                metric_data = combine_metric_data(
                    companies=top_companies,
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


async def write_excel_metrics(
    file_name: str, start_year: int, end_year: int, companies_metrics: dict,
) -> None:
    with pd.ExcelWriter(file_name) as writer:
        async for year in trange(
            start_year, end_year + 1, desc='Download companies by year',
        ):
            yearly_companies_data = {}

            for metric, company_metric in companies_metrics.items():
                metric_data = combine_metric_data(
                    companies=[
                        (i, company) for i, company in enumerate(company_metric.keys())
                    ],
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


async def main(arguments: Namespace):
    start_year, end_year = arguments.metrics_start_year, arguments.metrics_end_year
    if (
        start_year < config.METRICS_POSSIBLE_START_YEAR
        or start_year > config.METRICS_POSSIBLE_END_YEAR
    ):
        raise RuntimeError('start_year not in valid range')
    if (
        end_year < config.METRICS_POSSIBLE_START_YEAR
        or end_year > config.METRICS_POSSIBLE_END_YEAR
        or end_year < start_year
    ):
        raise RuntimeError('end_year not in valid range')

    companies_metrics, companies_names = {}, []
    async for metric_i in trange(
        len(config.METRICS_WITH_FILTER), desc='Download companies metrics',
    ):
        metric = config.METRICS_WITH_FILTER[metric_i]

        companies_metric = await get_companies_metrics(metric)
        if len(companies_names) == 0:
            companies_names = companies_metric.keys()
        companies_metrics[metric] = companies_metric

    await write_excel_top_400(
        file_name=arguments.output_file,
        start_year=start_year,
        end_year=end_year,
        companies_names=companies_names,
        companies_metrics=companies_metrics,
    )


if __name__ == '__main__':
    args = arg_parser.parse_args()
    basic_config(args.log_level, args.log_format, buffered=True)

    asyncio.run(main(args))
