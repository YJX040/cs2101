from googletrans import Translator

def detect_and_translate(text, translator, target_language):
    detected_language = translator.detect(text)
    if detected_language.lang in ['de', 'en', 'zh-CN', 'zh-TW']:
        translation = translator.translate(text, src=detected_language.lang, dest=target_language)
        translated_text = translation.text
        print(f"原始文本：{text}")
        print(f"翻译结果：{translated_text}")
    else:
        print("检测到输入文本语言不支持翻译。")

def main():
    target_language = 'zh-CN'  # 目标语言为中文简体
    translator = Translator()

    print("欢迎使用翻译测试程序！")
    print("请输入要翻译的文本（输入 q 退出）：")
    while True:
        user_input = input("> ")
        if user_input.lower() == 'q':
            print("感谢使用，再见！")
            break
        detect_and_translate(user_input, translator, target_language)

if __name__ == "__main__":
    main()
