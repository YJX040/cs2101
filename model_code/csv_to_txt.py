import csv

def csv_to_txt(csv_file, txt_file):
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        
        prev_subject = None  # 用于跟踪上一个subject的值
        
        with open(txt_file, 'w', encoding='utf-8') as txtfile:
            for row in reader:
                subject = row[0]
                predicate = row[1]
                obj = row[2]

                additional_info = ''
                if predicate == '属于':
                    additional_info = '属于' + obj + '博物馆，'
                elif predicate == '大小':
                    additional_info = '规模为' + obj + '，'
                elif predicate == '材料':
                    additional_info = '由' + obj + '制作而成,'
                elif predicate == '描述':
                    additional_info = '描述是' + obj + '。\n'
                elif predicate == '地理位置':
                    additional_info = '位于' + obj + '，'+''

                if subject != prev_subject:  # 如果当前subject与上一个subject不同，则输出完整行
                    txtfile.write(f"{subject}{additional_info}")
                else:  # 如果当前subject与上一个subject相同，则只输出附加信息
                    txtfile.write(f"{additional_info}")

                prev_subject = subject  # 更新prev_subject的值为当前subject

csv_file = './model_csv/output_museum_file.csv'
txt_file = './model_csv/museum_file.txt'

csv_to_txt(csv_file, txt_file)
