import csv

def convert_to_triplets(csv_file, output_file):

    material_subjects = {}# 存储相同材料的主体节点
    title_ids = {}  # 存储相同标题的 ID 号
    distinct_titles = set()  # 存储不同的标题
    
    # 检查文件路径
    print("CSV 文件路径:", csv_file)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Collection', 'Predicate', 'Material'])
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 检查数据格式
                title = row['title'].strip()
                if not title:
                    continue  # 跳过空的 title
                
                distinct_titles.add(title)  # 添加到不同的标题集合

                material = row['material'].strip()

                
                # 处理标题节点
                if title in title_ids:
                    title_id = f"{title}_{title_ids[title]}"
                    title_ids[title] += 1
                else:
                    title_id = title
                    title_ids[title] = 1
                
                # 处理材料节点
                if material:
                    if material in material_subjects:
                        writer.writerow([title_id, '材料', material_subjects[material]])
                    else:
                        material_subjects[material] = material
                        writer.writerow([title_id, '材料', material])

                
    
    return len(material_subjects)

# 示例用法
csv_file = './model_csv/museum_items_of_china_v2.csv'
output_file = './triples/material_triples.csv'
material_count= convert_to_triplets(csv_file, output_file)
print("不同材料的数量:", material_count)