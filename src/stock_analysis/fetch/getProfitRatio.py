import logging
import akshare as ak
import stock_analysis.constants as constants
logger = logging.getLogger(__name__)

# 筹码分布


def getRatio():
    stock_cyq_em_df = ak.stock_cyq_em(symbol=constants.SHENZHEN_MARKET, adjust="")
    logger.info(stock_cyq_em_df)