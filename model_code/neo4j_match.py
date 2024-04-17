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
            
            subject_node = Node("Subject", name=subject_name)
            object_node = Node("Object", name=object_name)
            
            subject_node.__primarylabel__ = "Subject"
            subject_node.__primarykey__ = "name"
            object_node.__primarylabel__ = "Object"
            object_node.__primarykey__ = "name"
            
            relation = Relationship(subject_node, predicate, object_node)
            
            graph.merge(subject_node)
            graph.merge(object_node)
            graph.merge(relation)
            
            subjects.add(subject_name)  # 添加主题到集合中
    
    return len(subjects)  # 返回不同主题的数量

# 示例用法
csv_file = 'output_file_germany.csv'
different_subjects_count = import_csv_to_neo4j(csv_file)
print("不同主题的数量:", different_subjects_count)
