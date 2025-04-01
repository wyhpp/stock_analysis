import logging
import akshare as ak
import stock_analysis.constants as constants
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False     # 解决负号'-'显示为方框的问题

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

def get_basic_market_data():
    # 获取基础行情数据
    # 截取2000年以后的数据，成交量数据不太对
    sh_df = ak.stock_zh_index_daily(symbol=constants.SHANGHAI_MARKET)
    sz_df = ak.stock_zh_index_daily(symbol=constants.SHENZHEN_MARKET)
    cy_df = ak.stock_zh_index_daily(symbol=constants.CHUANGYE_MARKET)
    market_data = pd.concat([sh_df, sz_df, cy_df]).groupby('date').agg({'volume':'sum'}).reset_index()
    return market_data

def get_market_data(start_date, end_date):
    """整合市场数据（网页7/8）"""
    
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
    
    all_data.sort(key=lambda r:r['日期'])
    merged_df = pd.DataFrame(all_data)
    # merged_df['日期'] = pd.to_datetime(merged_df['日期'])
    
    # 计算指标
    merged_df['涨停封板率'] = merged_df['涨停家数'] / (merged_df['涨停家数'] + merged_df['涨停炸板数']) * 100
    merged_df['跌停封板率'] = merged_df['跌停家数'] / (merged_df['跌停家数'] + merged_df['跌停炸板数']) * 100  # 防除零

    # merged_df.sort_values(key=lambda r:r['日期']) 
    
    return merged_df

#画图
def plot_basic_market_data(market_data):
    plt.figure(figsize=(14,6))
    plt.plot(market_data['date'], market_data['volume']/1e8, marker='o', color='#1f77b4')
    plt.title('全市成交量趋势（单位：亿元）', fontsize=14)
    plt.xlabel('日期', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_market_data(df):
    # 涨跌颜色反转
    fig, ax1 = plt.subplots(figsize=(14,6))

    ax1.bar(df['日期'], df['涨停家数'], color='#2ca02c', alpha=0.6, label='涨停')
    ax1.bar(df['日期'], -df['跌停家数'], color='#d62728', alpha=0.6, label='跌停')
    ax1.set_ylabel('家数', fontsize=12)
    ax1.legend(loc='upper left')

    # 添加涨跌停比例线
    ax2 = ax1.twinx()
    ax2.plot(df['日期'], df['涨停家数']/df['跌停家数'], 
            color='#9467bd', linestyle='--', marker='^')
    ax2.set_ylabel('涨跌停比', fontsize=12)

    plt.title('涨跌停家数对比分析', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_fengbanlv(df):
    plt.figure(figsize=(14,6))
    plt.plot(df['日期'], df['涨停封板率'], marker='o', linestyle='--', color='#17becf', label='涨停封板率')
    plt.plot(df['日期'], df['跌停封板率'], marker='s', linestyle='-.', color='#e377c2', label='跌停封板率')

    plt.fill_between(df['日期'], df['涨停封板率'], alpha=0.1, color='#17becf')
    plt.fill_between(df['日期'], df['跌停封板率'], alpha=0.1, color='#e377c2')

    plt.title('封板率趋势分析', fontsize=14)
    plt.ylabel('封板率(%)', fontsize=12)
    plt.ylim(0, 100)
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_lianban(df):
    # 日期从低到高排序
    plt.figure(figsize=(14,6))
    bars = plt.bar(df['日期'], df['最高连板数'], color='#ff7f0e', alpha=0.6)

    # 标注个股名称（网页3）
    for idx, rect in enumerate(bars):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., height+0.3,
                df.iloc[idx]['连板个股'],
                ha='center', va='bottom', rotation=45)

    plt.plot(df['日期'], df['最高连板数'], marker='o', color='#2c3e50')
    plt.title('最高连板数及龙头股追踪', fontsize=14)
    plt.ylabel('连板数', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()