import logging
import akshare as ak
logger = logging.getLogger(__name__)

def __init__(self, settings):
    self.settings = settings
    self.setup()

def get_summery():
    stock_sse_summary_df = ak.stock_sse_summary()
    logger.info(stock_sse_summary_df)

def a():
    return 1