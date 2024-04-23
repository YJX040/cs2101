import csv

def output_rows_with_null(csv_file):
    # 文件路径和对应的字段列表字典
    museum_fields = ['id', 'title', 'museum', 'era', 'material', 'size', 'description', 'detail_url', 'image', 'download_link']
    
    # 创建空列表来存储 'Staatliche Museen zu Berlin' 博物馆的行
    output_rows = []
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            museum = row['museum'].split(' ')[0]  # 使用 split() 方法提取博物馆名称的第一个部分
            if museum == 'Staatliche':
                # 检查是否存在空值
                if any(value.strip() == '' for key, value in row.items() if key in museum_fields):
                    output_rows.append([row[key] for key in museum_fields])

    # 将 'Staatliche Museen zu Berlin' 博物馆的行写入输出文件
    output_file = './model_csv/output_Staatliche_Museen_zu_Berlin_with_null.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(museum_fields)  # 写入标题行
        for row in output_rows:
            writer.writerow(row)

# 示例用法
csv_file = './model_csv/museum_items_of_china_v2.csv'
output_rows_with_null(csv_file)