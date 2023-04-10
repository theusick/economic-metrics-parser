"""
Type for uploading metrics from smart-lab
"""


class MetricType:
    """
    Class to represent metrics type
    """

    def __init__(self, rus_name: str, query_filter: str) -> None:
        self.__rus_name = rus_name
        self.__query_filter = query_filter

    @property
    def name(self) -> str:
        return self.__rus_name

    @property
    def filter(self) -> str:
        return self.__query_filter
