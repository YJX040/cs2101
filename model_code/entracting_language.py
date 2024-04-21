import pandas as pd
from langdetect import detect_langs

# 读取CSV文件
df = pd.read_csv('./model_csv/museum_germany.csv')

# 指定要遍历的列
columns_to_check = ['museum', 'title', 'era', 'material', 'size', 'description']

# 列出指定列的语言种类
language_set = set()
for column in columns_to_check:
    column_languages = set()
    for value in df[column]:
        try:
            languages = detect_langs(str(value))
            for lang in languages:
                column_languages.add(lang.lang)
        except Exception as e:
            pass
    language_set.update(column_languages)
    print(f"列 '{column}' 的语言种类：{column_languages}")

print("指定列的语言种类：", language_set)
