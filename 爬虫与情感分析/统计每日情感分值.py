import pandas as pd

# 读取情感分析结果数据
data = pd.read_excel('情感分析结果.xlsx')

# 将评论时间列转换为日期时间格式
data['评论时间'] = pd.to_datetime(data['评论时间'])

# 筛选出正面和负面的数据
positive_data = data[data['情感倾向'] == '正面']
negative_data = data[data['情感倾向'] == '负面']

# 按天汇总正面情感分值并计算加权分数
daily_positive_sentiment_score = positive_data.groupby(positive_data['评论时间'].dt.date)['情感分值'].sum()

# 按天汇总负面情感分值并计算加权分数
daily_negative_sentiment_score = negative_data.groupby(negative_data['评论时间'].dt.date)['情感分值'].sum()

# 计算正面加权分数与负面加权分数的总和
result_df = pd.DataFrame({
    '日期': daily_positive_sentiment_score.index,
    '正面加权分数': daily_positive_sentiment_score.values,
    '负面加权分数': daily_negative_sentiment_score.values,
    '总加权分数': daily_positive_sentiment_score.values + daily_negative_sentiment_score.values
})

# 保存结果到新的Excel文件
result_df.to_excel('每日情感加权分数.xlsx', index=False)
