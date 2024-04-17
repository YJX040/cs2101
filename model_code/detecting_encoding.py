import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        encoding_result = chardet.detect(raw_data)
        return encoding_result['encoding']

# 示例用法
csv_file = './model_csv/museum_germany.csv'
encoding = detect_encoding(csv_file)
print("CSV 文件编码为:", encoding)
