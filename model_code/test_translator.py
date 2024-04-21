import requests
import hashlib
import uuid
import time
from pypinyin import pinyin, Style
from googletrans import Translator

# 您的应用ID和应用密钥
APP_KEY = '00331485f57f0964'
APP_SECRET = 'vA89kuxxuFJ0ByMAKtB0pJpZ4lBv4Ipl'

def addAuthParams(app_key, app_secret, params):
    # 生成随机字符串
    salt = str(uuid.uuid4())
    # 获取当前时间戳
    curtime = str(int(time.time()))

    # 计算签名
    sign_str = app_key + params['q'] + salt + curtime + app_secret
    sign = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()

    # 添加认证参数
    params['appKey'] = app_key
    params['salt'] = salt
    params['sign'] = sign
    params['signType'] = 'v3'
    params['curtime'] = curtime

def detectLanguage(text):
    # 简单地检查文本中是否包含特定语言的常见字符
    # 这里根据已知的特征字符进行判断
    return 'auto'  # 如果无法确定语言，则返回 'auto' 表示自动识别

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    translated_text = translation.text
    return translated_text

def translate_with_pinyin(pinyin_text, target_language):
    # 创建 Translator 对象
    translator = Translator()
    # 将拼音字符串的首字母转换为小写
    pinyin_text_lower = pinyin_text.lower()
    # 翻译拼音为目标语言
    translation = translator.translate(pinyin_text_lower, dest=target_language)
    translated_text = translation.text
    return translated_text


def createRequest():
    q = 'LANDCARPET Europe'  # 待翻译文本
    lang_to = 'zh-cn'  # 目标语言语种，中文简体
    vocab_id = ''  # 您的用户词表ID，如果没有可以留空

    source_lang = detectLanguage(q)
    if source_lang != 'unknown':
        data = {'q': q, 'from': source_lang, 'to': lang_to, 'vocabId': vocab_id}
        addAuthParams(APP_KEY, APP_SECRET, data)

        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = doCall('https://openapi.youdao.com/api', header, data, 'post')
        result = str(res.content, 'utf-8')
        if 'errorCode' in result:
            print("翻译失败，尝试使用拼音翻译...")
            pinyin_text = chinese_to_pinyin(q)
            translated_text = translate_with_pinyin(pinyin_text, lang_to)
            print("翻译结果：", translated_text)
        else:
            print("翻译结果：", result)
    else:
        print("无法确定文本语言，输出原始文本：", q)

def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, headers=header)

def chinese_to_pinyin(text):
    # 将汉字转换为拼音
    pinyin_text = pinyin(text, style=Style.NORMAL)
    # 将拼音列表转换为字符串
    pinyin_str = ' '.join([item[0] for item in pinyin_text])
    return pinyin_str

if __name__ == '__main__':
    createRequest()
