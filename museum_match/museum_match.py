from py2neo import Graph, Node, Relationship
import csv

graph = Graph('bolt://8.130.118.241:7687', auth=("neo4j", "cs2101"))

def import_museum_to_neo4j(csv_file):
    museums = set()  # 用来存储不同的博物馆名称
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            museum_name = row['Subject']
            predicate = row['Predicate']
            object_name = row['Collection']
            
            # 检查数据库中是否已存在具有相同值的节点
            museum_node = graph.nodes.match("Museum", name=museum_name).first()
            object_node = graph.nodes.match("Collection", name=object_name).first()
            
            if museum_node is None:
                museum_node = Node("Museum", name=museum_name)
                graph.create(museum_node)
            
            # 将藏品作为博物馆的子节点，同时将属性作为藏品节点的属性
            if object_node is None:
                object_node = Node("Collection", name=object_name)
                graph.create(object_node)
            
            # 建立关系，确保博物馆与藏品之间的关联
            relation = Relationship(museum_node, predicate, object_node)
            graph.merge(relation)
            
            museums.add(museum_name)  # 添加博物馆名称到集合中
    
    return len(museums)  # 返回不同博物馆的数量

# 示例用法
csv_file = './triples/museum_triples.csv'
different_museums_count = import_museum_to_neo4j(csv_file)
print("不同博物馆的数量:", different_museums_count)
