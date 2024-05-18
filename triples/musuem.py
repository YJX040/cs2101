import csv

def convert_to_triplets(csv_file, output_file):
    museum_subjects = {}  # 存储相同博物馆的主体节点
    title_ids = {}  # 存储相同标题的 ID 号
    distinct_titles = set()  # 存储不同的标题
    
    # 检查文件路径
    print("CSV 文件路径:", csv_file)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Museum', 'Predicate', 'Collection'])
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 检查数据格式
                title = row['title'].strip()
                if not title:
                    continue  # 跳过空的 title
                
                distinct_titles.add(title)  # 添加到不同的标题集合
                
                museum = row['museum'].strip()
                
                # 处理标题节点
                if title in title_ids:
                    title_id = f"{title}_{title_ids[title]}"
                    title_ids[title] += 1
                else:
                    title_id = title
                    title_ids[title] = 1
                
                # 处理博物馆节点
                if museum:
                    if museum in museum_subjects:
                        writer.writerow([ museum_subjects[museum], '包含',title_id])
                    else:
                        museum_subjects[museum] = museum
                        writer.writerow([museum, '包含', title_id])
                
                
    
    return len(museum_subjects)
# 示例用法
csv_file = './model_csv/museum_items_of_china_v2.csv'
output_file = './triples/museum_triples.csv'
museum_count = convert_to_triplets(csv_file, output_file)
print("不同博物馆的数量:", museum_count)

