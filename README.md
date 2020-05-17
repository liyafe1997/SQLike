# SQLike
## 简体中文（Chinese Simplified）（English is in below down）
 
 一个用Python写的，基于平面文件（CSV）的，命令有点仿SQL的“数据库”。

甚至没有使用任何第三方的库，所有用到的模块都是Python默认环境下自带的模块。

与CSV有一点不同的事，第一行不是数据，而是列头。

支持开启TCP服务器，支持通过Socket发送SQL语句来执行。

由来呢，数据库课的课程设计，整天莫非就是搞什么XX管理系统，整天拿SQL SELECT来SELECT去，没什么意思。（老师也觉得没什么意思

（于是你们可以自主选题吧 （嗯那我干脆造一个数据库还有意思点（当然是for fun啦

Command Usage:

建表：

**CREATE TABLE _table_name (_column1,_column2,_column3…………)**

删库跑路：

**DROP TABLE _table_name**

插♂入数据：

**INSERT INTO _table_name VALUES (_data1,_data2_,_data3…………)**

更新数据(不带条件，更新表中该列所有数据) ：

**UPDATE _table_name SET _column=_data**

更新数据(带条件)：

**UPDATE _table_name SET _column=_data WHERE _column=_data**

删数据：

**DELETE FROM _table_name WHERE _column=_data**

检索所有列、所有数据：

**SELECT * FROM _table_name**

带条件检索所有列数据（支持AND/OR多个条件）：

**SELECT * FROM _table_name WHERE _column1=_data1 AND _column2=_data2 OR _column3=_data3**

不带条件，只检索某列所有数据：

**SELECT _column1,_column2 FROM _table_name**

带条件检索某列所有数据：

**SELECT _column1,_column2 FROM _table_name WHERE _column=_data**

检索并排序数据（仅需在SELECT命令的结尾添加ORDER BY _column） 例：

**SELECT _column1,_column2 FROM _table_name WHERE _column=_data ORDER BY _column1**

注：ORDER BY的数据必须为数字

降序检索数据（仅需在ORDER BY _column后加DESC） 例：

**SELECT * FROM _table_name ORDER BY _column1 DESC**

开启TCP Socket服务器 (Start TCP Socket Server)

**server BindIP:PORT (Example: server 127.0.0.1:1234)**

该TCP Socket服务器会响应客户端发来的SQL语句，返回结果，返回的结果与在SQLike终端中响应的一样（如Select请求返回的结果用换行符（\n）分割每一行即每条数据，包含表头；用TAB符（\t）分割列），自行试一下就知道了。

**也可直接通过参数启动Socket服务器: python SQLike.py server BindIP PORT (Example: python SQLike.py server 127.0.0.1 1234)**

## English 

 A simple "Database" based on flat CSV files and commands like "SQL", written by Python.

It doesn't need any third-part library, all modules used are python default environment built-in modules.

But it has a little differece with CSV, the first line is the colunm header, instead of data.

TCP Socket Server Supported. It can excuses SQL command via client sending.

The reason of make this, of course for fun hahahaha. It's a homework for my database course, And.. I want to make it fun so..

Command Usage:

Create table:

**CREATE TABLE _table_name (_column1,_column2,_column3…………)**

Delete a table:

**DROP TABLE _table_name**

Insert a row:

**INSERT INTO _table_name VALUES (_data1,_data2_,_data3…………)**

Update data without condition, means update all the data in the column:

**UPDATE _table_name SET _column=_data**

Update data with condition:

**UPDATE _table_name SET _column=_data WHERE _column=_data**

Delete a row:

**DELETE FROM _table_name WHERE _column=_data**

Query all the data with all columns:

**SELECT * FROM _table_name**

Query some data with all columns with a special condition (Support AND/OR multi condition):

**SELECT * FROM _table_name WHERE _column1=_data1 AND _column2=_data2 OR _column3=_data3**

Query all the data only with special single column:

**SELECT _column1,_column2 FROM _table_name**

Query some data only with special single column with a special condition:

**SELECT _column1,_column2 FROM _table_name WHERE _column=_data**

Query data and sort (Just add ORDER BY at the end of all kind of SELECT command) eg:

**SELECT _column1,_column2 FROM _table_name WHERE _column=_data ORDER BY _column1**

Note: ORDER BY must be a number

Sort in descending order (Just add DESC after ORDER BY _column) eg:

**SELECT * FROM _table_name ORDER BY _column1 DESC**

Start TCP Socket Server:

**server BindIP:PORT (Example: server 127.0.0.1:1234)**

This TCP Socket Server will response the SQL command sent from clients, the response as same as the SQL command result in the SQLike terminal. For example, The response of SELECT command is split by new line symbol (\n) for each line (include header), and by Tab symbol (\t) for each colunm. You can try yourself.

**You also can start socket server by using command arugments: python SQLike.py server BindIP PORT (Example: python SQLike.py server 127.0.0.1 1234)**
