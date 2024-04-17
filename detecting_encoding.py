import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        encoding_result = chardet.detect(raw_data)
        return encoding_result['encoding']

# 示例用法
csv_file = 'museum_knowledge_graph_museum_items_of_china.csv'
encoding = detect_encoding(csv_file)
print("CSV 文件编码为:", encoding)
