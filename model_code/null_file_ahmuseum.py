import csv

def output_rows_with_null(csv_file, museum_name):
    # 文件路径和对应的字段列表字典
    museums = {
        'Staatliche Museen zu Berlin': ['id', 'title', 'museum', 'era', 'material', 'size', 'description', 'detail_url', 'image', 'download_link'],
        'njmuseum': ['id', 'title', 'museum', 'size', 'description', 'geo', 'detail_url', 'image', 'download_link'],
        'ahmuseum': ['id', 'title', 'museum', 'era', 'description', 'geo', 'image', 'download_link']
    }
    
    # 确保博物馆名称在字典中
    if museum_name not in museums:
        print(f"Error: Museum '{museum_name}' not found in the dictionary.")
        return
    
    # 创建空列表来存储含有空值的行
    output_rows = []
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            museum = row['museum'].split(' ')[0]  # 使用 split() 方法提取博物馆名称的第一个部分
            if museum == museum_name:
                # 检查是否存在空值
                if any(value.strip() == '' for key, value in row.items() if key in museums[museum_name]):
                    output_rows.append([row[key] for key in museums[museum_name]])

    # 将含有空值的行写入输出文件
    output_file = f'./model_csv/output_{museum_name}_with_null.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(museums[museum_name])  # 写入标题行
        for row in output_rows:
            writer.writerow(row)

# 示例用法
csv_file = './model_csv/museum_items_of_china_v2.csv'
output_rows_with_null(csv_file, 'ahmuseum')
