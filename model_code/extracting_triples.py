import csv

def convert_to_triplets(csv_file, output_file):
    subjects = set()  # 用来存储不同的主体
    
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Subject', 'Predicate', 'Object'])
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row['title']
                if title is None:
                    continue  # 如果 title 为 None，则跳过当前行
                title = title.strip()
                museum = row['museum'].strip()
                era = row['era'].strip()
                material = row['material'].strip()
                size = row['size'].strip()
                description = row['description'].strip()
                image = row['image'].strip()
                detail_url = row['detail_url'].strip()
                
                # 检查所有数据是否都不为空，只有全部不为空才转换为三元组
                if title and museum and era and material and size and description and image and detail_url:
                    writer.writerow([title, '属于', museum])
                    writer.writerow([title, '年代', era])
                    writer.writerow([title, '材料', material])
                    writer.writerow([title, '大小', size])
                    writer.writerow([title, '描述', description])
                    writer.writerow([title, '图片链接', image])
                    writer.writerow([title, '详情链接', detail_url])
                    
                    subjects.add(title)  # 添加主体到集合中
    
    return len(subjects)  # 返回不同主体的数量

# 示例用法
csv_file = './model_csv/museum_germany.csv'
output_file = './model_csv/output_file_germany.csv'
different_subjects_count = convert_to_triplets(csv_file, output_file)
print("不同主体的数量:", different_subjects_count)
