# neo4j数据建模

使用工具:

* python3.9
  * py2neo
  * pandas
  * requests
  * bs4
  * csv
  * chardet

* neo4j-community(jdk11起步)

## 文件

* model_code
  * detecting_encoding.py
    * 识别文件编码（判断是不是utf-8）
  * extracting_triples.py  
    * 转换三元组
  * file_test.py
    * 测试能否自动填null
  * neo4j_clear_all.py
    * 清楚neo4j数据库所有节点
  * neo4j_match.py
    * neo4j数据库建立三元组
  * null_file.py
    * 提取csv内title存在，同时信息存在null的文物
* model_csv
  * museum_x.csv
    * 博物馆数据
      * _germany 柏林博物馆
  * output_x.csv
    * 输出文件
      * _updated 补充null后的文件
      * _germany 对应博物馆抓换后的三元组值
      * _null 空值文物，copy为测试file_test的数据

## 实现过程

1. 博物馆数据爬取完毕后，数据文件以utf-8格式导出csv，放入model_csv
2. 提取三元组，运行extracting_triples.py 
3. 三元组建模，连接neo4j数据库，运行neo4j_match.py
   1. 连接bolt://bolt://8.130.118.241:7687
   2. 账户：neo4j(community版本不修改的话，默认账户为neo4j)
   3. 密码：csxxxx(班级号)
4. 连接数据库，查看知识图谱效果

