import asyncio
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


async def get_top_companies(upload_year: int) -> list[tuple[int, str]]:
    async with ExpertScrapper() as scrapper:
        companies = await scrapper.scrap(upload_year)
        return companies


async def get_companies_metrics(metric: MetricType, companies_names: list[str]):
    async with SmartLabScrapper() as scrapper:
        companies_metrics = await scrapper.scrap(metric, companies=companies_names)
        return companies_metrics


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

    with pd.ExcelWriter(config.OUTPUT_DEFAULT_FILE) as writer:
        async for year in trange(start_year, end_year + 1, desc='Upload by year'):
            top_companies = await get_top_companies(year)

            yearly_companies_data = {}

            for metric in config.METRICS_WITH_FILTER:
                companies_metrics = await get_companies_metrics(
                    metric,
                    companies_names=[name for _, name in top_companies],
                )

                metric_data = combine_metric_data(
                    companies=top_companies,
                    metrics=companies_metrics,
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
    print(f'Successfully parsed data in {config.OUTPUT_DEFAULT_FILE}!')


if __name__ == '__main__':
    arguments = arg_parser.parse_args()
    basic_config(arguments.log_level, arguments.log_format, buffered=True)

    asyncio.run(main(arguments))
