from py2neo import Graph, Node, Relationship
import csv

graph = Graph('bolt://8.130.118.241:7687', auth=("neo4j", "cs2101"))

def import_csv_to_neo4j(csv_file):
    subjects = set()  # 用来存储不同的主题
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            subject_name = row['Subject']
            predicate = row['Predicate']
            object_name = row['Object']
            
            # 检查数据库中是否已存在具有相同值的节点
            subject_node = graph.nodes.match("Subject", name=subject_name).first()
            object_node = graph.nodes.match("Object", name=object_name).first()
            
            if subject_node is None:
                subject_node = Node("Subject", name=subject_name)
                graph.create(subject_node)
            
            if object_node is None:
                object_node = Node("Object", name=object_name)
                graph.create(object_node)
            
            relation = Relationship(subject_node, predicate, object_node)
            graph.merge(relation)
            
            subjects.add(subject_name)  # 添加主题到集合中
    
    return len(subjects)  # 返回不同主题的数量

# 示例用法
csv_file = './model_csv/output_museum_file.csv'
different_subjects_count = import_csv_to_neo4j(csv_file)
print("不同主题的数量:", different_subjects_count)
