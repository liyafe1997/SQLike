# SQLike
 A simple "Database" based on flat CSV files and commands like "SQL", written by Python.
 
 一个用Python写的，基于平面文件（CSV）的，命令有点仿SQL的“数据库”。

It doesn't need any third-part library, all modules used are python default environment built-in modules.

甚至没有使用任何第三方的库，所有用到的模块都是Python默认环境下自带的模块。

But it has a little differece with CSV, the first line is the colunm header, instead of data.

与CSV有一点不同的事，第一行不是数据，而是列头。

TCP Socket Server Supported. It can excuses SQL command via client sending.

支持开启TCP服务器，支持通过Socket发送SQL语句来执行。


由来呢，数据库课的课程设计，整天莫非就是搞什么XX管理系统，整天拿SQL SELECT来SELECT去，没什么意思。（老师也觉得没什么意思

（于是你们可以自主选题吧 （嗯那我干脆造一个数据库还有意思点


Command Usage:


建表(Create table)：

CREATE TABLE _table_name (_column1,_column2,_column3…………)


删库跑路(Delete a table)：

DROP TABLE _table_name


插♂入数据(Insert a row)：

INSERT INTO _table_name VALUES (_data1,_data2_,_data3…………)


更新数据(不带条件，更新表中该列所有数据) (Update data without condition, means update all the data in the column)：

UPDATE _table_name SET _column=_data


更新数据(带条件) (Update data with condition)：

UPDATE _table_name SET _column=_data WHERE _column=_data


删数据 (Delete a row)：

DELETE FROM _table_name WHERE _column=_data


检索所有列、所有数据 (Query all the data with all columns)：

SELECT * FROM _table_name


带条件检索所有列数据 (Query some data with all columns with a special condition)：

SELECT * FROM _table_name WHERE _column=_data


不带条件，只检索某列所有数据 (Query all the data only with special single column)：

SELECT _column1,_column2 FROM _table_name


带条件检索某列所有数据 (Query some data only with special single column with a special condition)：

SELECT _column1,_column2 FROM _table_name WHERE _column=_data

开启TCP Socket服务器 (Start TCP Socket Server)

server BindIP:PORT (Example: server 127.0.0.1:1234)

This TCP Socket Server will response the SQL command sent from clients, the response as same as the SQL command result in the SQLike terminal. For example, The response of SELECT command is split by new line symbol (\n) for each line (include header), and by Tab symbol (\t) for each colunm. You can try yourself.

该TCP Socket服务器会响应客户端发来的SQL语句，返回结果，返回的结果与在SQLike终端中响应的一样（如Select请求返回的结果用换行符（\n）分割每一行即每条数据，包含表头；用TAB符（\t）分割列），自行试一下就知道了。

