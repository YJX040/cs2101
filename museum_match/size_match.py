from py2neo import Graph, Node, Relationship
import csv

graph = Graph('bolt://8.130.118.241:7687', auth=("neo4j", "cs2101"))

def import_properties_to_neo4j(csv_file):
    properties = set()  # 用来存储不同的属性
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            subject_name = row['Collection']
            predicate = row['Predicate']
            object_name = row['Size']
            
            # 检查数据库中是否已存在具有相同值的节点
            subject_node = graph.nodes.match("Collection", name=subject_name).first()
            object_node = graph.nodes.match("Size", name=object_name).first()
            
            if object_node is None:
                object_node = Node("Size", name=object_name)
                graph.create(object_node)
            
            # 建立关系，确保藏品与属性之间的关联
            relation = Relationship(subject_node, predicate, object_node)
            graph.merge(relation)
            
            properties.add(object_name)  # 添加属性到集合中
    
    return len(properties)  # 返回不同属性的数量

# 示例用法
csv_file = './triples/size_triples.csv'
different_properties_count = import_properties_to_neo4j(csv_file)
print("不同属性的数量:", different_properties_count)
