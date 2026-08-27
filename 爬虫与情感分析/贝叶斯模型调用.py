import joblib
import jieba
import pandas as pd
import string
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

vect = joblib.load('./vectorizer.pkl')
nb = joblib.load('./nb_model.pkl')


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 设置负号正常显示
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
dt = DecisionTreeClassifier(max_depth=10)

# 分词函数
def chinese_word_cut(mytext):
    text = " ".join(jieba.cut(mytext))
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# 获取停用词表
def get_custom_stopwords(stop_words_file):
    with open(stop_words_file, 'r', encoding='utf-8') as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [i for i in stopwords_list]
    return custom_stopwords_list

stop_words_file = './哈工大停用词表.txt'
stopwords = get_custom_stopwords(stop_words_file)

# 分析数据
data = pd.read_csv('./清洗后的小米su7评论合.csv', encoding='utf-8')

data = data[pd.notnull(data['评论内容'])]  # 过滤掉空值
data = data[data['评论内容'].apply(lambda x: isinstance(x, str))]  # 过滤掉非字符串类型的数据

data['关键词'] = data.评论内容.apply(chinese_word_cut)
data['关键词'] = data['关键词'].str.rstrip('。')
X = data['关键词']
X_vec = vect.transform(X)
nb_result = nb.predict(X_vec)
data['情感倾向'] = nb_result

# 使用predict_proba获取概率预测结果
nb_result_proba = nb.predict_proba(X_vec)
emotion_scores = nb_result_proba[:, 1]
data['情感分值'] = emotion_scores

# 根据情感分值划分情感倾向
data.loc[data['情感分值'] <= 0.20, '情感倾向'] = '负面'
data.loc[(data['情感分值'] > 0.20) & (data['情感分值'] <= 0.6), '情感倾向'] = '中性'
data.loc[data['情感分值'] > 0.6, '情感倾向'] = '正面'

# 转换情感分值的范围
data['情感分值'] = (data['情感分值'] - 0.5) * 2
data.loc[data['情感倾向'] == '中性', '情感分值'] = 0
data['情感分值'] = data['情感分值'] * 100

# 处理点赞数量对情感分值的影响
data['情感分值'] = data.apply(lambda row: row['情感分值'] + row['点赞数量'] * 0.1 if row['情感倾向'] == '正面' else row['情感分值'], axis=1)
data['情感分值'] = data.apply(lambda row: row['情感分值'] + row['点赞数量'] * -0.1 if row['情感倾向'] == '负面' else row['情感分值'], axis=1)

def add_points(row):
    if row['情感倾向'] == '正面':
        return row['情感分值'] + 20
    else:
        return row['情感分值']

# 应用加分函数
data['情感分值'] = data.apply(add_points, axis=1)
# 保留情感分值保留七位小数
data['情感分值'] = data['情感分值'].round(7)

data.to_excel('情感分析结果.xlsx', index=False)
