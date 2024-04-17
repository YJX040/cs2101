import csv

def output_rows_with_null(csv_file, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(['title', 'museum', 'era', 'material', 'size'])
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 检查 title 是否为空，如果为空，则跳过当前行
                if row['title'].strip() == '':
                    continue
                # 检查是否存在空值
                if any(value.strip() == '' for key, value in row.items() if key!='dascription' and key != 'image' and key != 'detail_url'):
                    writer.writerow([row['title'], row['museum'], row['era'], row['material'], 
                                     row['size']])

# 示例用法
csv_file = 'museum_germany.csv'
output_file = 'output_file_with_null.csv'
output_rows_with_null(csv_file, output_file)
