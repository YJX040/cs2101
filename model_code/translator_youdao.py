import pandas as pd
import requests
import hashlib
import uuid
import time
import socket
from pypinyin import pinyin, Style
from googletrans import Translator

# 有道智云翻译API的应用ID和应用密钥
APP_KEY = '00331485f57f0964'
APP_SECRET = 'vA89kuxxuFJ0ByMAKtB0pJpZ4lBv4Ipl'

# 定义超时重试次数和重试间隔
MAX_RETRIES = 3
RETRY_INTERVAL = 5  # seconds

def translate_text_youdao(text, lang_to):
    # 生成随机字符串
    salt = str(uuid.uuid4())
    # 获取当前时间戳
    curtime = str(int(time.time()))

    # 计算签名
    sign_str = APP_KEY + text + salt + curtime + APP_SECRET
    sign = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()

    # 构造请求参数
    data = {
        'q': text,
        'from': 'auto',
        'to': lang_to,
        'appKey': APP_KEY,
        'salt': salt,
        'sign': sign,
        'signType': 'v3',
        'curtime': curtime
    }

    retries = 0
    while retries < MAX_RETRIES:
        try:
            # 发送POST请求
            response = requests.post('https://openapi.youdao.com/api', data=data)
            # 解析响应结果
            translation_result = response.json()
            # 检查是否有翻译结果
            if 'translation' in translation_result:
                translated_text = translation_result['translation'][0]
                return translated_text
            else:
                return None
        except (socket.timeout, TimeoutError) as e:
            print(f"超时异常，重试中 ({retries+1}/{MAX_RETRIES})...")
            retries += 1
            time.sleep(RETRY_INTERVAL)
    print("达到最大重试次数，放弃翻译。")
    return None

def translate_text_with_pinyin(text, lang_to):
    # 将文本转换为拼音
    pinyin_text = pinyin(text, style=Style.NORMAL)
    pinyin_str = ' '.join([item[0] for item in pinyin_text]).lower()  # 将拼音转换为小写
    # 使用谷歌翻译将拼音翻译为目标语言
    translator = Translator()
    translation = translator.translate(pinyin_str, dest=lang_to)
    translated_text = translation.text
    return translated_text

# 加载中间结果文件（如果存在）
normal_termination = False  # 默认为异常结束
header = True  # 默认需要写入表头
try:
    intermediate_df = pd.read_csv('./model_csv/museum_translated_youdao_partial_file.csv')
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
    with open('./model_csv/museum_translated_youdao_partial_file.csv', 'r', encoding='utf-8') as f:
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

# 读取CSV文件
df = pd.read_csv('./model_csv/louvre.csv')

# 指定要翻译的列名
columns_to_translate = [
    'Inventory number',
    'Collection',
    'Artist/maker / School / Artistic centre',
    'Object name/Title',
    'Type of object',
    'Description/Features',
    'Inscriptions',
    'Dimensions',
    'Materials and techniques',
    'Date',
    'Place of origin',
    'Collector / Previous owner / Commissioner / Archaeologist / Dedicatee',
    'Acquisition details',
    'Acquisition date',
    'Owned by',
    'Held by',
    'Current location',
    'Mode d\'acquisition',
    'Period',
    'Places',
    'Type',
]


# 设置翻译结束的行数
end_index = 4800

# 设置目标语言
target_language = 'zh-cn'  # 中文（简体）

# 遍历指定行范围内的每个值，翻译成中文并替换原始值
for index, row in df.iterrows():
    if index < start_index:
        continue
    if index > end_index:
        break

    translation_status = 1  # 默认为全部翻译成功

    for column_name in columns_to_translate:
        # 检查值是否不为空且非中文
        if pd.notnull(row[column_name]) and not row[column_name].encode('utf-8').isalpha():
            # 自动识别语言并进行翻译
            translated_text = translate_text_youdao(row[column_name], target_language)
            if translated_text:
                df.at[index, column_name] = translated_text
                print(f"翻译成功：{column_name} - {row[column_name]} -> {translated_text}")
            else:
                print(f"自动识别语言失败，尝试拼音翻译：{column_name} - {row[column_name]}")
                # 拼音翻译并将首字母转换为小写
                translated_text_pinyin = translate_text_with_pinyin(row[column_name], target_language)
                df.at[index, column_name] = translated_text_pinyin
                print(f"拼音翻译结果：{translated_text_pinyin}")
        else:
            print(f"{column_name} 为空或已经是中文")

    # 在每次迭代后将结果写入文件
    df.iloc[start_index:index+1].to_csv('./model_csv/museum_translated_youdao_partial_file.csv', index=False)

# 将结果写入CSV文件
df.to_csv('./model_csv/museum_translated_youdao_file.csv', index=False)

# 更新正常结束状态文件
pd.DataFrame([normal_termination], columns=['normal_termination']).to_csv('./model_csv/normal_termination_youdao_status.csv',
                                                                          index=False)

# 写入正常结束标志
if normal_termination:
    with open('./model_csv/termination_youdao_status.txt', 'w') as f:
        f.write('1')
else:
    with open('./model_csv/termination_youdao_status.txt', 'w') as f:
        f.write('0')
