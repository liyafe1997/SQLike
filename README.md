# SQLike
 A simple "Database" based on flat files and commands like "SQL", written by Python.
 
 一个用Python写的，基于平面文件的，命令有点仿SQL的“数据库”。


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

DELETE _table_name WHERE _column=_data


检索所有列、所有数据 (Query all the data with all columns)：

SELECT * FROM _table_name


带条件检索所有列数据 (Query some data with all columns with a special condition)：

SELECT * FROM _table_name WHERE _column=_data


不带条件，只检索某列所有数据 (Query all the data only with special single column)：

SELECT _column=_data FROM _table_name


带条件检索某列所有数据(Query some data only with special single column with a special condition)：

SELECT _column=_data FROM _table_name WHERE _column=_data
