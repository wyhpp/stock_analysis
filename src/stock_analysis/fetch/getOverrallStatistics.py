import logging
import akshare as ak
import stock_analysis.constants as constants
import pandas as pd
from datetime import datetime, timedelta
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

# 成交量 同比上日，涨跌停家数（折线图），涨停封板率，跌停封板率，最高连板（折线图）
# 竞价数据，一字板数，掉单率，跌幅大于9%个股数，竞价金额

def fetch_zt_data(dates):
    """获取多日涨停板数据（网页2/3/7）"""
    all_data = []
    for date in dates:
        try:
            df = ak.stock_zt_pool_em(date=date.strftime("%Y%m%d"))
            df['日期'] = date
            # 过滤ST股和新股（网页3）
            df = df[~df['名称'].str.contains('ST|退市|N')]
            all_data.append(df)
            logger.info("all_data",all_data)
        except Exception as e:
            print(f"获取{date}数据失败：{str(e)}")
    return pd.concat(all_data)

def fetch_dt_data(dates):
    """获取多日跌停板数据（网页2/3/7）"""
    all_data = []
    for date in dates:
        try:
            df = ak.stock_dtgc_pool_em(date=date.strftime("%Y%m%d"))
            df['日期'] = date
            # 过滤ST股和新股（网页3）
            df = df[~df['名称'].str.contains('ST|退市|N')]
            all_data.append(df)
            logger.info("all_data",all_data)
        except Exception as e:
            print(f"获取{date}数据失败：{str(e)}")
    return pd.concat(all_data)

def get_market_data(start_date, end_date):
    """整合市场数据（网页7/8）"""
    
    # 获取基础行情数据
    sh_df = ak.stock_zh_index_daily(symbol="sh000001")
    sz_df = ak.stock_zh_index_daily(symbol="sz399106")
    market_data = pd.concat([sh_df, sz_df]).groupby('date').agg({'volume':'sum'}).reset_index()
    
 # 获取交易日历（网页1方案）
    trade_date_df = ak.tool_trade_date_hist_sina()
    trade_date_df = pd.to_datetime(trade_date_df['trade_date'])
    trade_dates = trade_date_df.dt.strftime('%Y%m%d').tolist()
    # 生成完整日期范围
    date_range = pd.date_range(start=start_date, end=end_date, freq='D').strftime('%Y%m%d').tolist()
    date_range = list(set(date_range) & set(trade_dates))
    all_data = []
    for date in date_range:
        try:
            # 获取涨停数据（网页1/6）
            zt_df = ak.stock_zt_pool_em(date=date)
            # 获取跌停数据（网页2/3）
            dt_df = ak.stock_zt_pool_dtgc_em(date=date)
            
            # 合并数据
            daily_stats = {
                '日期': date,
                '涨停家数': len(zt_df),
                '跌停家数': len(dt_df),
                '涨停炸板数': zt_df['炸板次数'].sum(),
                '跌停炸板数': dt_df['开板次数'].sum(),
                '最高连板数': zt_df['连板数'].max(),
                '连板个股': zt_df.loc[zt_df['连板数'].idxmax(), '名称'] if not zt_df.empty else None
            }
            all_data.append(daily_stats)
        except Exception as e:
            print(f"获取{date}数据失败：{e}")
    
    merged_df = pd.DataFrame(all_data)
    # merged_df['日期'] = pd.to_datetime(merged_df['日期'])
    
    # 计算指标
    merged_df['涨停封板率'] = merged_df['涨停家数'] / (merged_df['涨停家数'] + merged_df['涨停炸板数']) * 100
    merged_df['跌停封板率'] = merged_df['跌停家数'] / (merged_df['跌停家数'] + merged_df['跌停炸板数']) * 100  # 防除零
    
    return merged_df
