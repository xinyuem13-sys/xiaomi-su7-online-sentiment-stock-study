import numpy as np
import pandas as pd
import jieba
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
import joblib


# 读取数据
data = pd.read_excel('标注集.xlsx')

dt_model = DecisionTreeClassifier(max_depth=10)

# 分词函数
def chinese_word_cut(text):
    cut_text = " ".join(jieba.cut(text))
    cut_text = cut_text.translate(str.maketrans('', '', string.punctuation))
    return cut_text

# 对评论进行分词
data['分词结果'] = data.评论.apply(chinese_word_cut)

# 获取停用词表
def load_custom_stopwords(stop_words_file, encoding='utf-8'):
    with open(stop_words_file, encoding=encoding) as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [word for word in stopwords_list]
    return custom_stopwords_list

stop_words_file = '哈工大停用词表.txt'
stopwords = load_custom_stopwords(stop_words_file, encoding='utf-8')

# 构建词频矩阵
vectorizer = CountVectorizer(max_df=0.8, min_df=3, token_pattern=u'(?u)\\b[^\\d\\W]\\w+\\b', stop_words=frozenset(stopwords))
X = data['分词结果']
y = data.情感倾向
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=22)

# 训练朴素贝叶斯模型
nb_model = MultinomialNB()
X_train_vectorized = vectorizer.fit_transform(X_train)
nb_model.fit(X_train_vectorized, y_train)
train_accuracy = nb_model.score(X_train_vectorized, y_train)
dt_model.fit(X_train_vectorized, y_train)

# 保存模型和向量器
joblib.dump(nb_model, './nb_model.pkl')
joblib.dump(vectorizer, './vectorizer.pkl')


