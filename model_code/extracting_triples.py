import csv

def convert_to_triplets(csv_file, output_file):
    museum_subjects = {}  # 存储相同博物馆的主体节点
    era_subjects = {}     # 存储相同年代的主体节点
    size_subjects = {}    # 存储相同大小的主体节点
    material_subjects = {}# 存储相同材料的主体节点
    description_subjects = {}  # 存储相同描述的主体节点
    geo_subjects = {}  # 存储相同地理位置的主体节点
    title_ids = {}  # 存储相同标题的 ID 号
    distinct_titles = set()  # 存储不同的标题
    
    # 检查文件路径
    print("CSV 文件路径:", csv_file)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['Subject', 'Predicate', 'Object'])
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 检查数据格式
                title = row['title'].strip()
                if not title:
                    continue  # 跳过空的 title
                
                distinct_titles.add(title)  # 添加到不同的标题集合
                
                museum = row['museum'].strip()
                era = row['era'].strip()
                material = row['material'].strip()
                size = row['size'].strip()
                description = row['description'].strip()
                geo = row['geo'].strip()  # 新增的地理位置字段
                
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
                        writer.writerow([title_id, '属于', museum_subjects[museum]])
                    else:
                        museum_subjects[museum] = museum
                        writer.writerow([title_id, '属于', museum])
                
                # 处理年代节点
                if era:
                    if era in era_subjects:
                        writer.writerow([title_id, '年代', era_subjects[era]])
                    else:
                        era_subjects[era] = era
                        writer.writerow([title_id, '年代', era])
                
                # 处理大小节点
                if size:
                    if size in size_subjects:
                        writer.writerow([title_id, '大小', size_subjects[size]])
                    else:
                        size_subjects[size] = size
                        writer.writerow([title_id, '大小', size])
                
                # 处理材料节点
                if material:
                    if material in material_subjects:
                        writer.writerow([title_id, '材料', material_subjects[material]])
                    else:
                        material_subjects[material] = material
                        writer.writerow([title_id, '材料', material])
                
                  # 处理地理位置节点
                if geo:
                    if geo in geo_subjects:
                        writer.writerow([title_id, '地理位置', geo_subjects[geo]])
                    else:
                        geo_subjects[geo] = geo
                        writer.writerow([title_id, '地理位置', geo])

                # 处理描述节点
                if description:
                    if description in description_subjects:
                        writer.writerow([title_id, '描述', description_subjects[description]])
                    else:
                        description_subjects[description] = description
                        writer.writerow([title_id, '描述', description])
                
              
    
    return len(museum_subjects), len(era_subjects), len(size_subjects), len(material_subjects),len(geo_subjects),len(description_subjects), len(distinct_titles)

# 示例用法
csv_file = './model_csv/museum_items_of_china_v2.csv'
output_file = './model_csv/output_museum_file.csv'
museum_count, era_count, size_count, material_count,geo_count,decription_count, distinct_title_count = convert_to_triplets(csv_file, output_file)
print("不同博物馆的数量:", museum_count)
print("不同年代的数量:", era_count)
print("不同大小的数量:", size_count)
print("不同材料的数量:", material_count)
print("不同地理位置的数量:", geo_count)
print("不同描述的数量:", decription_count)
print("不同藏品的数量:", distinct_title_count)
