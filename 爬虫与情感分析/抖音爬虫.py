import time
import os
import requests
import csv

# 请求头
headers = {
    'accept': "application/json, text/plain, */*",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    'cookie': os.environ.get('DOUYIN_COOKIE', '')
}


# 发送爬取请求
def spider(url, params):
    response = requests.get(url, headers=headers, params=params)
    response.encoding = 'utf-8'
    return response.json()


# 时间戳转换成日期
def get_time(ctime):
    timeArray = time.localtime(ctime)
    otherStyleTime = time.strftime("%Y.%m.%d", timeArray)
    return str(otherStyleTime)


# 保存评论
def sava_data(comment, aweme_id):
    global comment_count


    try:
        ip_label = comment['ip_label']
    except:
        ip_label = '未知'

    try:
        user_name = comment['user']['nickname'].strip()
    except:
        user_name = '无'

    data_dict = {
        "用户名": user_name,
        "视频链接": f"https://www.douyin.com/video/{aweme_id}",
        "评论时间": get_time(comment['create_time']),
        "IP属地": ip_label,
        "点赞数量": comment['digg_count'],
        "评论内容": comment['text'].strip().replace('\n', '')
    }

    # 评论数量+1
    comment_count += 1

    print(f"当前评论数: {comment_count}\n",
          f"用户名：{data_dict['用户名']}\n",
          f"视频链接：{data_dict['视频链接']}\n",
          f"评论时间：{data_dict['评论时间']}\n",
          f"IP属地：{data_dict['IP属地']}\n",
          f"点赞数量：{data_dict['点赞数量']}\n",
          f"评论内容：{data_dict['评论内容']}\n"
          )
    writer.writerow(data_dict)


# 爬取评论
def get_comments(aweme_id):
    cursor = 0
    page = 0
    while True:
        params = {
            'aid': 6383,
            'cursor': cursor,
            'aweme_id': aweme_id,
            'count': 20,
        }

        url = f'https://www.douyin.com/aweme/v1/web/comment/list?'

        # 爬一次就睡1秒
        time.sleep(1)
        json_data = spider(url, params)

        if json_data['comments'] is None:
            break

        for comment in json_data['comments']:
            sava_data(comment, aweme_id)

        if not json_data['has_more']:
            break

        # 下一页评论的地址
        cursor = cursor + 20

        # 每爬完一页，页数加1
        page = page + 1
        print('================爬取Page{}完毕================'.format(page))


def search_keyword(keyword):
    offset = 0
    count = 16
    while True:
        params = {
            'aid': 6383,
            'channel': 'channel_pc_web',
            'search_channel': 'aweme_video_web',
            'keyword': keyword,
            'offset': offset,
            'publish_time': 0,  # 0：不限时间  1：一天内  7：一周内  182：半年内
            'sort_type': 1,  # 0：综合排序  1：最多点赞 2：最新发布
            'is_filter_search': 0,  # 0：不筛选  1：筛选
            'count': count,
        }

        url = f'https://www.douyin.com/aweme/v1/web/search/item/?'

        # 爬一次就睡1秒
        time.sleep(1)
        json_data = spider(url, params)

        for video_data in json_data['data']:
            print(f"正在爬取 {video_data['aweme_info']['desc']} 的评论\n")
            time.sleep(1)

            aweme_id = video_data['aweme_info']['aweme_id']
            get_comments(aweme_id)

        if json_data['has_more'] == 0:
            print(json_data)
            break

        offset = offset + count
        count = 10


if __name__ == '__main__':
    comment_count = 0
    keyword = '小米su7'  # 要爬取的关键词

    # 向csv文件写入表头  评论数据csv文件
    header = ["用户名", "视频链接", "评论时间", "IP属地", "点赞数量", "评论内容"]
    f = open(f"抖音{keyword}评论.csv", "w", encoding="utf-8-sig", newline="")
    writer = csv.DictWriter(f, header)
    writer.writeheader()

    search_keyword(keyword)
