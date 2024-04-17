import pandas as pd
import requests
from bs4 import BeautifulSoup

# 读取CSV文件
df = pd.read_csv('./model_csv/output_file_with_null_copy.csv')

# 定义函数：根据标题获取信息
def get_info_from_baidu(title):
    # 构建百度搜索的URL
    search_url = f'https://www.baidu.com/s?wd={title}'
    
    # 发送请求并获取搜索结果页面内容
    response = requests.get(search_url)
    if response.status_code == 200:
        print(f'搜索成功：{search_url}')  # 输出搜索成功的信息
        # 使用Beautiful Soup解析页面内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 在搜索结果中查找相关信息
        # 这里以查找搜索结果的第一个标题为例
        result = soup.find('h3', {'class': 't'})
        if result:
            link = result.find('a')['href']
            print(f'找到相关信息：{link}')  # 输出找到相关信息的链接
            return link
        else:
            print('未找到相关信息')  # 输出未找到相关信息的提示
            return None
    else:
        print(f'搜索失败：{search_url}')  # 输出搜索失败的信息
        return None

# 循环处理每一行数据
for index, row in df.iterrows():
    # 获取标题
    title = row['title']
    
    # 获取标题对应的信息
    link = get_info_from_baidu(title)
    if link:
        # 在这里可以继续处理搜索结果页面内容，提取你需要的信息
        # 这里只是简单地将搜索结果链接填充到df中的detail_url列
        df.at[index, 'detail_url'] = link
    
# 将更新后的数据写回CSV文件
df.to_csv('./model_csv/output_baidu_updated.csv', index=False)
