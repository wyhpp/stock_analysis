import pytest
import logging
from stock_analysis.fetch import getOverrallStatistics
from stock_analysis.fetch import getProfitRatio
from stock_analysis.fetch import getSectorStatistics



# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def test_base():
#     val = getOverrallStatistics.get_summery()

# def test_ratio():
#     val = getProfitRatio.getRatio()

def test_plot():
    getSectorStatistics.plot_pie(getSectorStatistics.inflow_top5, "资金净流入TOP5板块", ['#4CAF50', '#81C784', '#A5D6A7', '#C8E6C9', '#E8F5E9'])
# 资金流出饼图（红色系）
    getSectorStatistics.plot_pie(getSectorStatistics.outflow_top5, "资金净流出TOP5板块", ['#EF5350', '#EF9A9A', '#FFCDD2', '#FFEBEE', '#FF8A80'])
