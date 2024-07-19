import pytest
import logging
from stock_analysis.fetch import getOverrallStatistics
from stock_analysis.fetch import getProfitRatio


# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_base():
    val = getOverrallStatistics.get_summery()

def test_ratio():
    val = getProfitRatio.getRatio()
    