#!/usr/bin/env python
import codecs
import os
import socket
import threading

lock = threading.Lock()


def Command(cmd):
    try:
        c = cmd.split(" ")
        if c[0].upper() == "CREATE" and c[1].upper() == "TABLE":
            if not len(c) == 4:
                return -1
            if not c[3][0] == "(":
                return -1
            if not c[3][-1] == ")":
                return -1
            return CreateTable(c[2], c[3][1:-1])
        elif c[0].upper() == "DROP" and c[1].upper() == "TABLE":
            if not len(c) == 3:
                return -1
            return DropTable(c[2])
        elif c[0].upper() == "INSERT" and c[1].upper() == "INTO" and c[3].upper() == "VALUES":
            if not len(c) == 5:
                return -1
            if not c[4][0] == "(":
                return -1
            if not c[4][-1] == ")":
                return -1
            return Insert(c[2], c[4])
        elif c[0].upper() == "SELECT" and c[2].upper() == "FROM":
            if len(c) == 6:
                if not len(c[5].split("=")) == 2:
                    return -1
                return Select(c[3], c[1], c[5])
            elif len(c) == 4:
                return Select(c[3], c[1], 0)
            else:
                return -1

        elif c[0].upper() == "DELETE" and c[1].upper() == "FROM" and c[3].upper() == "WHERE":
            if not len(c) == 5:
                return -1
            if not len(c[4].split("=")) == 2:
                return -1
            return DeleteData(c[2], c[4])
        elif c[0].upper() == "UPDATE" and c[2].upper() == "SET":
            if not len(c[3].split("=")) == 2:
                return -1
            if len(c) == 6:
                if not len(c[5].split("=")) == 2:
                    return -1
                return UpdateData(c[1], c[3], c[5])
            else:
                return UpdateData(c[1], c[3], 0)

        else:
            return -1
    except:
        return -1


def UpdateData(tablename, set, where):
    try:
        dbdata = ReadFile(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + tablename)
    except:
        return "Error: No this table!"
    dbdata = dbdata.split("\n")
    dbdata = [line for line in dbdata if line.strip()] 
    SetColumn = set.split("=")[0]
    SetValue = set.split("=")[1]
    VIndex = FindColumnIndex(SetColumn, dbdata[0].split(","))
    if VIndex == -1:
        return "Error: In SET no this column!!"
    count = 0
    for i in range(1, len(dbdata)):
        EachData = dbdata[i].split(",")
        if len(EachData) == len(dbdata[0].split(",")):
            if not where == 0:
                WhereColumn = where.split("=")[0]
                WhereValue = where.split("=")[1]
                CIndex = FindColumnIndex(WhereColumn, dbdata[0].split(","))
                if CIndex == -1:
                    return "Error: In WHERE no this column!!"

                if EachData[CIndex] == WhereValue:
                    count += 1
                    EachData[VIndex] = SetValue
                    newData = ""
                    for j in range(len(EachData)):
                        newData += EachData[j] + ","
                    newData = newData[0:-1]
                    dbdata[i] = newData
                    # UpdateLine(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + tablename, i, newData)
            else:
                EachData[VIndex] = SetValue
                count += 1
                newData = ""
                for j in range(len(EachData)):
                    newData += EachData[j] + ","
                newData = newData[0:-1]
                dbdata[i] = newData
                # UpdateLine(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + tablename, i, newData)
    WriteFileArray(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + tablename, dbdata)
    return str(count) + " Row(s) Updated"


def DeleteData(tablename, where):
    try:
        dbdata = ReadFile(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + tablename)
    except:
        return "Error: No this table!"
    dbdata = dbdata.split("\n")
    WhereColumn = where.split("=")[0]
    WhereValue = where.split("=")[1]
    CIndex = FindColumnIndex(WhereColumn, dbdata[0].split(","))
    if CIndex == -1:
        return "Error: In WHERE no this column!!"
    count = 0
    for i in range(len(dbdata)):
        EachData = dbdata[i].split(",")
        if len(EachData) == len(dbdata[0].split(",")):
            if EachData[CIndex] == WhereValue:
                count += 1
                dbdata[i] = ""
                # DeleteLine(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + tablename, i)
    DeleteEmptyLine(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + tablename, dbdata)
    return "Deleted " + str(count) + " Row(s)"



def DeleteEmptyLine(filename, content):
    WriteFile(filename, "")
    file_object = codecs.open(filename, 'a', "utf-8")
    for i in range(len(content)):
        if content[i] != "":
            file_object.write(unicode(content[i]) + "\n")
    file_object.close()


def WriteFileArray(filename, content):
    WriteFile(filename, "")
    file_object = codecs.open(filename, 'a', "utf-8")
    for i in range(len(content)):
        file_object.write(unicode(content[i]) + "\n")
    file_object.close()


def CreateTable(name, colunm):
    if os.path.exists(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + name):
        return "Error: Table already existed!"

    else:
        WriteFileLine(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + name, colunm + "\n")
    return "Table " + name + " Created!"


def DropTable(name):
    if not os.path.exists(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + name):
        return "Error: Table not existed!"

    else:
        os.remove(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + name)
        return "Table " + name + " Droped!"


def Insert(tablename, data):
    try:
        dbdata = ReadFile(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + tablename)
    except:
        return "Error: No this table!"
    dbdata = dbdata.split("\n")
    colunms = dbdata[0].split(",")
    incomingdata = data.split(",")
    if len(incomingdata) != len(colunms):
        return "Error: Length of your input VALUES and table colunms not match!"

    else:
        WriteFileLine(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + tablename, data[1:-1] + "\n")
        return "A row Inserted"


def Select(tablename, selectcolumn, where):
    try:
        AllData = ReadFile(os.path.split(os.path.abspath(__file__))[0]+"/DB/" + tablename).split("\n")
        AllData = [line for line in AllData if line.strip()] 
    except:
        return "Error: No this table!"
    Columns = AllData[0].split(",")
    ReturnDatas = ""
    if not selectcolumn[0] == "*":
        for i in range(len(Columns)):
            if Columns[i] in selectcolumn:
                ReturnDatas += Columns[i] + "\t"
    else:
        for i in range(len(Columns)):
            ReturnDatas += Columns[i] + "	"
    ReturnDatas += "\n"
    for i in range(1, len(AllData)):
        if selectcolumn == "*":
            if where == 0:
                ReturnDatas += AllData[i].replace(",", "\t") + "\n"
            else:
                WhereColumn = where.split("=")[0]
                WhereValue = where.split("=")[1]
                CIndex = FindColumnIndex(WhereColumn, Columns)
                if CIndex == -1:
                    return "Error: In WHERE no this column!!"

                EachData = AllData[i].split(",")
                if len(EachData) == len(AllData[0].split(",")):
                    if EachData[CIndex] == WhereValue:
                        ReturnDatas += AllData[i].replace(",", "\t") + "\n"
        else:
            SingleLineData = AllData[i].split(",")
            if where == 0:
                for j in range(len(SingleLineData)):
                    if Columns[j] in selectcolumn:
                        ReturnDatas += SingleLineData[j] + "\t"
                ReturnDatas += "\n"
            else:
                WhereColumn = where.split("=")[0]
                WhereValue = where.split("=")[1]
                CIndex = FindColumnIndex(WhereColumn, Columns)
                if CIndex == -1:
                    return "Error: In WHERE no this column!!"

                EachData = AllData[i].split(",")
                if len(EachData) == len(AllData[0].split(",")):
                    if EachData[CIndex] == WhereValue:
                        for j in range(len(SingleLineData)):
                            if Columns[j] in selectcolumn:
                                ReturnDatas += SingleLineData[j] + "\t"
                        ReturnDatas += "\n"
    return ReturnDatas


def FindColumnIndex(column, columns):
    for i in range(len(columns)):
        if columns[i] == column:
            return i
    return -1


def ReadFile(filename):
    file_object = open(filename)
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()
    return all_the_text.decode("utf-8")


def WriteFile(filename, content):
    if not os.path.exists(filename):
        try:
            os.mkdir(os.path.dirname(filename))
        except:
            pass
        try:
            os.mknod(filename)
        except:
            pass
    file_object = codecs.open(filename, 'w', "utf-8")
    file_object.write(unicode(content))
    file_object.close()


def WriteFileLine(filename, content):
    if not os.path.exists(filename):
        try:
            os.mkdir(os.path.dirname(filename))
        except:
            pass
        try:
            os.mknod(filename)
        except:
            pass
    file_object = codecs.open(filename, 'a', "utf-8")
    file_object.write(content)
    file_object.close()


def StartSocketServer(IP, port):
    server = socket.socket()
    ip_port = (IP, port)
    server.bind(ip_port)
    server.listen(5)
    sthread = threading.Thread(target=SocketBind, args=(server,))
    sthread.setDaemon(True)
    sthread.start()
    print "Bind at " + IP + ":" + str(port)


def SocketBind(ss):
    while True:
        conn, addr = ss.accept()
        latestconn = conn
        recvsthread = threading.Thread(target=SocketReceiving, args=(conn,))
        recvsthread.setDaemon(True)
        recvsthread.start()


def SocketReceiving(incomingconn):
    try:
        while True:
            data = incomingconn.recv(1024)
            if lock.acquire():
                result = Command(str(data))
                lock.release()
            if result == -1:
                incomingconn.send("SQLike Command Format Error!")
            else:
                incomingconn.send(str(result))
    except:
        pass


if __name__ == '__main__':
    print "Welcome To SQLike 0.0005 Alpha"
    print "Enter \"QUIT\" or \"EXIT\" To Exit This Program"
    print "Enter \"HELP\" to show help"
    while 1:
        cmd = raw_input("SQLike>>> ")
        cmd = str(cmd)
        if cmd.lower() == "quit" or cmd.lower() == "exit":
            exit(0)
        elif cmd == "":
            pass
        elif cmd.lower() == "help":
            print "Command Usage:"
            print ""
            print "1 Create table:"
            print "  CREATE TABLE _table_name (_column1,_column2,_column3....)"
            print ""
            print "2 Delete a table:"
            print "  DROP TABLE _table_name"
            print ""
            print "3 Insert a row:"
            print "  INSERT INTO _table_name VALUES (_data1,data2,_data3....)"
            print ""
            print "4 Update data without condition, means update all the data in the column:"
            print "  UPDATE _table_name SET _column=_data"
            print ""
            print "5 Update data with condition:"
            print "  UPDATE _table_name SET _column=_data WHERE _column=_data"
            print ""
            print "6 Delete a row:"
            print "  DELETE FROM _table_name WHERE _column=_data"
            print ""
            print "7 Query all the data with all columns:"
            print "  SELECT * FROM _table_name"
            print ""
            print "8 Query some data with all columns with a special condition:"
            print "  SELECT * FROM _table_name WHERE _column=_data"
            print ""
            print "9 Query all the data only with special column(s):"
            print "  SELECT _column1,_column2 FROM _table_name"
            print ""
            print "10 Query some data only with special single column with a special condition:"
            print "  SELECT _column1,_column2 FROM _table_name WHERE _column=_data"
            print ""
            print "11 Start TCP Socket Server"
            print "  server BindIP:PORT"
            print "  Example: server 0.0.0.0:1666"
            print ""
        elif cmd.split(" ")[0].lower() == "server":
            if len(cmd.split(" ")) == 2:
                if len(cmd.split(" ")[1].split(":")) == 2:
                    StartSocketServer(cmd.split(" ")[1].split(":")[0], int(cmd.split(" ")[1].split(":")[1]))
                    print "TCP Socket Server Started !"
                else:
                    print("SQLike Command Format Error!")
            else:
                print("SQLike Command Format Error!")

        else:
            if lock.acquire():
                cmdResult = Command(cmd)
                if cmdResult == -1:
                    print("SQLike Command Format Error!")
                else:
                    print cmdResult
                lock.release()
