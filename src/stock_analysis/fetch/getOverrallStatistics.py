import logging
import akshare as ak
import stock_analysis.constants as constants
logger = logging.getLogger(__name__)

def __init__(self, settings):
    self.settings = settings
    self.setup()

# 获取上证、深证收盘数据
def get_summery():
    # 获取上证指数日线数据（网页5的QUANTAXIS类似逻辑）
    sz_index = ak.stock_zh_index_daily(symbol=constants.SHANGHAI_MARKET)
    # 获取深证成指日线数据
    szcz_index = ak.stock_zh_index_daily(symbol=constants.SHENZHEN_MARKET)
    logger.info("上海指数:",sz_index,"深证指数:",szcz_index)
    return sz_index, szcz_index