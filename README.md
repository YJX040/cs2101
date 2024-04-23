# neo4j数据建模

使用工具:

* python3.9
  * py2neo
  * pandas
  * requests
  * bs4
  * csv
  * chardet
  * googletrans
  * googletrans

* neo4j-community(jdk11起步)

## 文件

* model_code
  * detecting_encoding.py
    
    * 识别文件编码（判断是不是utf-8）
    
  * detecting_language.py
  
    * 搜索文件内有的语言个数，便于翻译时知道可能会出现的结果
    * 有不少拼音，这种调用api翻译的时候就可以注意一下
  
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
    
  * translator_google/youdao
    * 调用Google机器翻译（除了id和url，img以外的列都翻译）
    * 超时或者中断直接重新运行，会继续上次记录继续翻译
    
    * 有道的api，但翻译效果一般，不如上一个
    
  * jpg_change
    
    * 修改成2400*2400
    
  * csv_to_txt
  
    * 生成藏品的介绍语句，用于问答api输入
    * txt_part就是提取出来一部分，测试api输入后的结果
  
  * null_file_xxmuseum
  
    * 进行数据不补充时查看还有多少null值
  
  * 
  
* model_csv
  * museum_x.csv
    * 博物馆数据
  * output_x.csv
    * 输出文件
      * _updated 补充null后的文件
      * _germany 对应博物馆抓换后的三元组值
      * _null 空值文物，copy为测试file_test的数据
      * _museum是三元组，建模用的
  * output_file.txt
    * 测试输入用的txt
    * random就是随机提取多少行


## 实现过程

1. 博物馆数据爬取完毕后，数据文件以utf-8格式导出csv，放入model_csv
2. 提取三元组，运行extracting_triples.py 
3. 三元组建模，连接neo4j数据库，运行neo4j_match.py
   1. 连接bolt://bolt://8.130.118.241:7687
   2. 账户：neo4j(community版本不修改的话，默认账户为neo4j)
   3. 密码：csxxxx(班级号)
4. 连接数据库，查看知识图谱效果