import requests
import pandas as pd
from googletrans import Translator
import time
import socket
import os

# 定义超时重试次数和重试间隔
MAX_RETRIES = 5
RETRY_INTERVAL = 10  # seconds

def translate_with_retry(text, translator, source_language, target_language):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            if text is None:
                raise ValueError("翻译文本不能为空")
            translation = translator.translate(text, src=source_language, dest=target_language)
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

# 读取CSV文件
df = pd.read_csv('./model_csv/museum_germany.csv')

# 指定要翻译的列名
columns_to_translate = ['museum', 'title', 'era', 'material', 'size', 'description']

# 设置从第几行开始翻译
start_index = 0

# 设置翻译结束的行数
end_index = 4827

# 设置源语言和目标语言
source_language = 'de'
target_language = 'zh-cn'

# 创建翻译器
translator = Translator()

# 加载中间结果文件（如果存在）
normal_termination = False  # 默认为异常结束
header = True  # 默认需要写入表头
try:
    intermediate_df = pd.read_csv('./model_csv/museum_translated_file_partial.csv')
    if intermediate_df.empty:
        print("中间结果文件为空。")
        start_index = 0
    else:
        start_index = intermediate_df.index[-1] + 1  # 获取上次中断的索引后继续
        print(f"加载中间结果文件成功，从第 {start_index} 行继续翻译。")
        header = False  # 不需要写入表头
        normal_termination = True  # 文件存在，表示正常结束
except pd.errors.ParserError:
    print("中间结果文件存在解析错误，尝试跳过错误的行并继续加载数据。")
    # 尝试跳过错误的行并加载数据
    with open('./model_csv/museum_translated_file_partial.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        try:
            intermediate_df = pd.DataFrame([line.split(',') for line in lines])
            if intermediate_df.empty:
                print("中间结果文件为空。")
                start_index = 0
            else:
                start_index = intermediate_df.index[-1] + 1  # 获取上次中断的索引后继续
                print(f"加载中间结果文件成功，从第 {start_index} 行继续翻译。")
                header = False  # 不需要写入表头
                normal_termination = True  # 文件存在，表示正常结束
        except Exception as e:
            print(f"无法处理错误的行: {e}")
            start_index = 0
except FileNotFoundError:
    print("中间结果文件不存在，从头开始翻译。")
    start_index = 0


# 遍历指定行范围内的每个值，翻译成中文并替换原始值
for index, row in df.iterrows():
    if index < start_index:
        continue
    if index > end_index:
        break

    translation_status = 1  # 默认为全部翻译成功

    for column_name in columns_to_translate:
        # 检查值是否不为空且为源语言
        if pd.notnull(row[column_name]) and row[column_name] != '':
            text_to_translate = row[column_name]
            # 添加错误处理机制
            if text_to_translate.strip() != '':
                try:
                    detected_language = translator.detect(text_to_translate)
                    if detected_language is not None and detected_language.lang == source_language:
                        translated_text = translate_with_retry(text_to_translate, translator, source_language, target_language)
                        if translated_text:
                            df.at[index, column_name] = translated_text
                            print(f"翻译成功：{column_name} - {text_to_translate} -> {translated_text}")
                        else:
                            translation_status = 0  # 存在翻译失败的情况
                            print(f"翻译失败：{column_name} - {text_to_translate}")
                    else:
                        print(f"{column_name} 不是 {source_language} 文本：{text_to_translate}")
                except Exception as e:
                    print(f"发生异常：{e}")
            else:
                print(f"{column_name} 为空或非 {source_language} 文本")
                translation_status = 0  # 存在空文本


    # 在DataFrame中添加翻译状态列
    df.at[index, 'translation_status'] = translation_status

    # 在每次迭代后将结果写入文件
    if index == start_index and header:  # 只在第一次写入时写入列名
        df.iloc[start_index:index + 1].to_csv('./model_csv/museum_translated_file_partial.csv', mode='a', index=False,
                                              encoding='utf-8-sig')
    else:
        df.iloc[[index]].to_csv('./model_csv/museum_translated_file_partial.csv', mode='a', index=False, header=False,
                                encoding='utf-8-sig')
    if translation_status == 1:
        if os.path.exists('./model_csv/museum_translated_file.csv'):
            df.iloc[[index]].to_csv('./model_csv/museum_translated_file.csv', mode='a', header=False, index=False, encoding='utf-8-sig')
        else:
            df.iloc[[index]].to_csv('./model_csv/museum_translated_file.csv', mode='a', header=True, index=False, encoding='utf-8-sig')


    # 更新正常结束状态文件
    pd.DataFrame([normal_termination], columns=['normal_termination']).to_csv('./model_csv/normal_termination_status.csv',
                                                                              index=False)

# 过滤出已经翻译的行，然后将结果写入最终输出文件


# 写入正常结束标志
if normal_termination:
    with open('./model_csv/termination_status.txt', 'w') as f:
        f.write('1')
else:
    with open('./model_csv/termination_status.txt', 'w') as f:
        f.write('0')


# 英语：en 中文（简体）：zh-cn 中文（繁体）：zh-tw 法语：fr 德语：de 西班牙语：es 日语：ja 韩语：ko 俄语：ru 葡萄牙语：pt
