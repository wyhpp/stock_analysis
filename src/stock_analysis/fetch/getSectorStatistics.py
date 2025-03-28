import logging
import akshare as ak
import stock_analysis.constants as constants
import matplotlib.pyplot as plt
logger = logging.getLogger(__name__)

# 获取行业板块资金流向数据（今日）
fund_flow_df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
logger.info(fund_flow_df);
# 筛选关键字段
fund_flow_df = fund_flow_df[['名称', '今日主力净流入-净额', '今日涨跌幅']]
# 计算资金净流入（单位：亿元）
fund_flow_df['资金净流入'] = fund_flow_df['今日主力净流入-净额'] / 1e8

# 资金流入TOP5
inflow_top5 = fund_flow_df[fund_flow_df['资金净流入'] > 0].nlargest(5, '资金净流入')
# 资金流出TOP5
outflow_top5 = fund_flow_df[fund_flow_df['资金净流入'] < 0].nsmallest(5, '资金净流入')
# 涨跌幅TOP5（正负各取前5）
gain_top5 = fund_flow_df.nlargest(5, '今日涨跌幅')
loss_top5 = fund_flow_df.nsmallest(5, '今日涨跌幅')

# 资金流入饼图
def plot_pie(data, title, colors):
    labels = data['名称']
    sizes = abs(data['资金净流入'])
    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.title(title)
    plt.axis('equal')
    plt.show()

# 资金流入饼图（绿色系）
plot_pie(inflow_top5, "资金净流入TOP5板块", ['#4CAF50', '#81C784', '#A5D6A7', '#C8E6C9', '#E8F5E9'])
# 资金流出饼图（红色系）
plot_pie(outflow_top5, "资金净流出TOP5板块", ['#EF5350', '#EF9A9A', '#FFCDD2', '#FFEBEE', '#FF8A80'])

# 涨跌幅饼图
def plot_gain_loss_pie(gain_data, loss_data):
    combined_labels = list(gain_data['名称']) + list(loss_data['名称'])
    combined_sizes = list(gain_data['今日涨跌幅']) + list(abs(loss_data['今日涨跌幅']))
    colors = ['#4CAF50']*5 + ['#EF5350']*5  # 绿色为涨幅，红色为跌幅
    plt.figure(figsize=(12, 8))
    plt.pie(combined_sizes, labels=combined_labels, autopct='%1.1f%%', colors=colors)
    plt.title("涨跌幅TOP5板块（绿色：涨幅｜红色：跌幅）")
    plt.axis('equal')
    plt.show()

plot_gain_loss_pie(gain_top5, loss_top5)



