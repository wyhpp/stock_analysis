import pytest
import logging
from stock_analysis.fetch import getOverrallStatistics

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_base():
    val = getOverrallStatistics.get_summery()

    