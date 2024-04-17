'''
Author: Fhx0902 fanhaoxin0902@qq.com
Date: 2024-04-16 16:20:37
LastEditors: Fhx0902 fanhaoxin0902@qq.com
LastEditTime: 2024-04-16 23:50:12
FilePath: \venu_cs2101\cs_2101\test\match.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
 
 
from py2neo import Graph
def del_all_graph(graph):
    #删除节点
    # 图中所有节点及关系都删除
    y = input("请确认是否要删除图库中所有节点及关系（y/n）：")
    if y == 'y':
        graph.delete_all()
        print("已确认删除图库所有节点和关系\n")
    elif y == 'n':
        print("已确认不删除图库所有节点和关系\n")
        pass
    else:
        print("=========请输入正确的提示引导=========\n")
        del_all_graph(graph)
 
 
 
 
if __name__ == '__main__':
    # 连接图库
    graph = Graph('bolt://8.130.118.241:7687', auth=('neo4j', 'cs2101'))
    # 确认是否删除图库所有节点
    del_all_graph(graph)