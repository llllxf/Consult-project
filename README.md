# geo-bot

### 系统主要架构：

采用问答系统主流的nlu,dialog management,nlg架构，图谱存储在rdf4j,由于rdf4j只有java接口，而问答系统使用python实现，所以问答系统有两个后端，一个是python实现的问答后端，一个是查询图谱的java后端，两个后端通过接口连接

![Image text](https://github.com/llllxf/geo-bot/raw/master/backend/pic/%E6%9E%B6%E6%9E%84.png)

### 系统流程

![Image text](https://github.com/llllxf/geo-bot/raw/master/backend/pic/%E6%B5%81%E7%A8%8B.png)


#### 问答系统目前可以处理一般问题，计算问题和比较问题(最值问题视为计算问题)

#### 是否问题

![Image text](https://github.com/llllxf/geo-bot/raw/master/backend/pic/%E5%9B%BE%E7%89%875.jpg)

![Image text](https://github.com/llllxf/geo-bot/raw/master/backend/pic/4.png)

#### 计算问题

![Image text](https://github.com/llllxf/geo-bot/raw/master/backend/pic/3.png)

![Image text](https://github.com/llllxf/geo-bot/blob/master/backend/pic/1.png)

![Image text](https://github.com/llllxf/geo-bot/raw/master/backend/pic/2.png)

#### 比较问题
![Image text](https://github.com/llllxf/geo-bot/blob/master/backend/pic/1.png)


