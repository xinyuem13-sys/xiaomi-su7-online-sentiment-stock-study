import re
import pandas as pd
import random
import jieba

# 加载停用词表
stopwords_file = '哈工大停用词表.txt'
with open(stopwords_file, "r", encoding='utf-8') as words:
    stopwords = [i.strip() for i in words]


def clean_text(text):
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
    text = re.sub(r"\[\S+\]", "", text)  # 去除表情符号
    URL_REGEX = re.compile(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
        re.IGNORECASE)
    text = re.sub(URL_REGEX, "", text)  # 去除网址
    text = re.sub(r"\s+", " ", text)  # 合并正文中过多的空格
    text = re.sub(r'[^\u4e00-\u9fa5]', '', text)  # 保留中文字符
    return text.strip()

def segment_text(text):
    words = jieba.cut(text)
    words = [word for word in words if word not in stopwords]  # 过滤停用词
    return ' '.join(words)

def format_date(date_str):
    parts = date_str.split('/')
    year = parts[0]
    month = parts[1]
    day = parts[2].split()[0]  # 去除时间部分
    return f'{year}-{month.zfill(2)}-{day.zfill(2)}'  # 使用zfill填充月份和日期的0

if __name__ == '__main__':
    file_name = '小米su7评论合.csv'
    data = pd.read_csv(file_name)

    # 修改评论时间的格式
    data['评论时间'] = data['评论时间'].apply(format_date)

    comments = data['评论内容'].apply(lambda x: str(x))
    clean_comments = comments.apply(clean_text)
    data['评论内容'] = clean_comments

    # 分词并添加关键词列
    data['关键词'] = data['评论内容'].apply(segment_text)

    columns_to_save = ['用户名', '评论时间', 'IP属地', '点赞数量', '评论内容', '关键词']
    final_data = data[columns_to_save]
    final_data = final_data[final_data['评论内容'].notna() & (final_data['评论内容'] != '')]
    cleaned_file_name = f'清洗后的{file_name}'
    final_data.to_csv(cleaned_file_name, index=False, encoding='utf-8-sig')
    print(f'数据清洗并分词完毕，清洗后的文件已保存为{cleaned_file_name}')
