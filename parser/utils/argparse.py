"""
Contains methods for argparse processing
"""
from argparse import Action, ArgumentDefaultsHelpFormatter, ArgumentParser
from parser.config import ParserMode, config

from aiomisc.log import LogFormat, LogLevel


class ValidateStartYear(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < config.METRICS_POSSIBLE_START_YEAR:
            parser.error(f'argument -sy/--start-year: invalid int value: {values}')
        setattr(namespace, self.dest, values)


class ValidateEndYear(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < config.METRICS_POSSIBLE_END_YEAR:
            parser.error(f'argument -ey/--end-year: invalid int value: {values}')
        setattr(namespace, self.dest, values)


arg_parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

group = arg_parser.add_argument_group('Parser options')
group.add_argument(
    '-m',
    '--mode',
    type=ParserMode,
    default=ParserMode.TOP_400,
    choices=list(ParserMode),
    dest='mode',
    help='Parser modes',
)
group.add_argument(
    '-sy',
    '--start-year',
    type=int,
    default=2013,
    action=ValidateStartYear,
    dest='metrics_start_year',
    help='Economic metrics upload start year. In range 2013-2022',
)
group.add_argument(
    '-ey',
    '--end-year',
    type=int,
    default=2022,
    action=ValidateEndYear,
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
