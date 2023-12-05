import sys

from loguru import logger as _logger

from appgen.utils.const import PROJECT_ROOT

def define_log_level(print_level="INFO", logfile_level="DEBUG"):
    """
       Adjust the log level to above level
       Source: https://github.com/geekan/MetaGPT/blob/main/metagpt/logs.py
    """
    _logger.remove()
    _logger.add(sys.stderr, level=print_level)
    _logger.add(PROJECT_ROOT / 'logs/log.txt', level=logfile_level)
    return _logger

logger = define_log_level()
