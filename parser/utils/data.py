from parser.utils import MetricType


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
