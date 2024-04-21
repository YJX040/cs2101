import requests
import pandas as pd
from googletrans import Translator
import time
import socket
import os

# 定义超时重试次数和重试间隔
MAX_RETRIES = 5
RETRY_INTERVAL = 10  # seconds

def translate_with_retry(text, translator, target_language):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            if text is None:
                raise ValueError("翻译文本不能为空")
            translation = translator.translate(text, dest=target_language)
            translated_text = translation.text
            return translated_text
        except (socket.timeout, TimeoutError, requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            print(f"发生异常: {type(e).__name__}")
            print(f"超时异常，重试中 ({retries+1}/{MAX_RETRIES})...")
            retries += 1
            time.sleep(RETRY_INTERVAL)
        except ValueError as ve:
            print(f"发生异常: {ve}")
            return None
    print("达到最大重试次数，放弃翻译。")
    return None

# 创建翻译器
translator = Translator()

# 读取CSV文件
df = pd.read_csv('./model_csv/museum_germany.csv')

# 设置从第几行开始翻译
start_index = 0

# 设置翻译结束的行数
end_index = 100

# 指定要翻译的列名
columns_to_translate = ['museum', 'title', 'era', 'material', 'size', 'description']

# 创建一个空的DataFrame，用于存储翻译后没有空值的行
output_df = pd.DataFrame(columns=df.columns)

# 遍历指定行范围内的每个值，翻译成中文并替换原始值
for index, row in df.iterrows():
    if index < start_index:
        continue
    if index > end_index:
        break

    translation_status = 1  # 默认为全部翻译成功

    for column_name in columns_to_translate:
        # 检查值是否不为空
        if pd.notnull(row[column_name]) and row[column_name] != '':
            text_to_translate = row[column_name]
            # 添加错误处理机制
            if text_to_translate.strip() != '':
                try:
                    detected_language = translator.detect(text_to_translate)
                    if detected_language is not None:
                        target_language = 'zh-cn'  # 目标语言为中文简体
                        translated_text = translate_with_retry(text_to_translate, translator, target_language)
                        if translated_text:
                            df.at[index, column_name] = translated_text
                            print(f"翻译成功：{column_name} - {text_to_translate} -> {translated_text}")
                        else:
                            translation_status = 0  # 存在翻译失败的情况
                            print(f"翻译失败：{column_name} - {text_to_translate}")
                    else:
                        print(f"无法识别 {column_name} 的语言：{text_to_translate}")
                except Exception as e:
                    print(f"发生异常：{e}")
            else:
                print(f"{column_name} 为空")
                translation_status = 0  # 存在空文本

    # 在DataFrame中添加翻译状态列
    df.at[index, 'translation_status'] = translation_status

    # 如果翻译后没有空值，则将该行添加到 output_df 中
    if translation_status == 1:
        output_df = output_df.append(row, ignore_index=True)

    # 在每次迭代后将结果写入文件
    df.iloc[[index]].to_csv('./model_csv/museum_translated_partial.csv', mode='a', index=False, header=False, encoding='utf-8-sig')

# 将 output_df 写入到 output_file_finish.csv 文件中
output_df.to_csv('./model_csv/output_file_finish.csv', index=False, encoding='utf-8-sig')

# 过滤出已经翻译的行，然后将结果写入最终输出文件

# 写入正常结束标志
with open('./model_csv/termination_status.txt', 'w') as f:
    f.write('1')
