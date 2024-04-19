import pandas as pd
import re

# 读取 CSV 文件
df = pd.read_csv('./model_csv/museum_germany.csv')

# 定义替换函数
def replace_url(url):
    if isinstance(url, str):
        return re.sub(r'(\d+)x(\d+).jpg', '2400x2400.jpg', url)
    else:
        return url

# 修改 image 列的 URL
df['image'] = df['image'].apply(replace_url)

# 修改 download_link 列的 URL
df['download_link'] = df['download_link'].apply(replace_url)

# 将修改后的数据写回 CSV 文件
df.to_csv('./model_csv/jpg_change.csv', index=False)
