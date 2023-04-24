import asyncio
import logging
from argparse import Namespace
from parser.config import ParserMode, config
from parser.scrappers import ExpertScrapper, SmartLabScrapper
from parser.utils import MetricType, write_excel_data
from parser.utils.argparse import arg_parser

import pandas as pd
from aiomisc.log import basic_config
from tqdm.asyncio import trange


log = logging.getLogger(__name__)


async def get_top_companies(upload_year: int, **kwargs) -> list[tuple[int, str]]:
    async with ExpertScrapper() as scrapper:
        companies = await scrapper.scrap(upload_year, **kwargs)
        return companies


async def get_companies_metrics(metric: MetricType, **kwargs):
    async with SmartLabScrapper() as scrapper:
        companies_metrics = await scrapper.scrap(metric, **kwargs)
        return companies_metrics


async def get_companies_names_with_metrics(
    metrics: list,
    **kwargs,
) -> tuple[dict, list]:
    companies_metrics, companies_names = {}, []
    async for metric_i in trange(
        len(metrics),
        desc='Download companies metrics',
    ):
        metric = metrics[metric_i]

        companies_metric = await get_companies_metrics(metric, **kwargs)
        if len(companies_names) == 0:
            companies_names = companies_metric.keys()
        companies_metrics[metric] = companies_metric
    return (companies_metrics, companies_names)


async def main(arguments: Namespace):
    metrics = config.DIVIDENDS_METRICS_WITH_FILTER
    if arguments.mode == ParserMode.RAS:
        metrics = config.RAS_METRICS_WITH_FILTER

    companies_metrics, companies_names = await get_companies_names_with_metrics(
        metrics=metrics,
        url_mixin=config.RAS_URL_MIXIN,
    )

    companies, functor_get_top_companies = None, None
    if arguments.mode == ParserMode.TOP_400:
        companies, functor_get_top_companies = companies_names, get_top_companies

    await write_excel_data(
        file_name=arguments.output_file,
        start_year=arguments.metrics_start_year,
        end_year=arguments.metrics_end_year,
        companies_metrics=companies_metrics,
        companies=companies,
        functor_get_top_companies=functor_get_top_companies,
    )


if __name__ == '__main__':
    args = arg_parser.parse_args()
    basic_config(args.log_level, args.log_format, buffered=True)

    asyncio.run(main(args))
