import pytest
import logging
from stock_analysis.fetch import getOverrallStatistics
from datetime import datetime, timedelta
import akshare as ak
import pandas as pd



# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_plot():
    # 获取最近30天数据
    end_date = datetime.now()
    start_date = end_date - timedelta(days=4)
    df = getOverrallStatistics.get_market_data(start_date,end_date)
    print(df)