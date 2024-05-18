import csv

def convert_to_triplets(csv_file, output_file):

    geo_subjects = {}  # 存储相同地理位置的主体节点
    title_ids = {}  # 存储相同标题的 ID 号
    distinct_titles = set()  # 存储不同的标题
    
    # 检查文件路径
    print("CSV 文件路径:", csv_file)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Collection', 'Predicate', 'Geo'])
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 检查数据格式
                title = row['title'].strip()
                if not title:
                    continue  # 跳过空的 title
                
                distinct_titles.add(title)  # 添加到不同的标题集合

                geo = row['geo'].strip()  # 新增的地理位置字段
                
                # 处理标题节点
                if title in title_ids:
                    title_id = f"{title}_{title_ids[title]}"
                    title_ids[title] += 1
                else:
                    title_id = title
                    title_ids[title] = 1
                
                #   处理地理位置节点
                if geo:
                    if geo in geo_subjects:
                        writer.writerow([title_id, '地理位置', geo_subjects[geo]])
                    else:
                        geo_subjects[geo] = geo
                        writer.writerow([title_id, '地理位置', geo])


    
    return len(geo_subjects)

# 示例用法
csv_file = './model_csv/museum_items_of_china_v2.csv'
output_file = './triples/geo_triples.csv'
geo_count = convert_to_triplets(csv_file, output_file)

print("不同地理位置的数量:", geo_count)

