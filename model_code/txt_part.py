import random

# 读取原始文件的内容
with open('./model_csv/museum_file.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 随机选择100行
random_lines = random.sample(lines, 100)

# 输出到新文件
with open('./model_csv/museum_file_random.txt', 'w', encoding='utf-8') as f:
    f.writelines(random_lines)
