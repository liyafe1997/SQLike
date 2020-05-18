#!/usr/bin/env python3
import codecs
import os
import socket
import threading
import sys
import signal
try:
    import readline  #for support input history
except:
    pass  #readline not available

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
            if len(c) > 4:
                #                if not len(c[5].split("=")) == 2:
                #                    return -1
                #                return Select(c[3], c[1], c[5])
                return Select(c[3], c[1], c[4:])
            elif len(c) == 4:
                return Select(c[3], c[1], 0)
        elif c[0].upper() == "DELETE" and c[1].upper() == "FROM" and c[3].upper() == "WHERE":
            return DeleteData(c[2], c[4:])
        elif c[0].upper() == "UPDATE" and c[2].upper() == "SET":
            if not len(c[3].split("=")) == 2:
                return -1
            if len(c) > 5:
                if not len(c[5].split("=")) == 2:
                    return -1
                return UpdateData(c[1], c[3], c[4:])
            elif len(c) == 4:
                return UpdateData(c[1], c[3], 0)

        else:
            return -1
    except:
        return -1


def UpdateData(tablename, set, wherelist):
    WhereConditionList = []
    WhereLogic = []
    #Process Where List
    if (wherelist != 0):
        for i in range(len(wherelist)):
            if ("=" in wherelist[i]):
                WhereConditionList.append(wherelist[i])
                if (i + 1 < len(wherelist)):
                    WhereLogic.append(wherelist[i + 1].upper())
                else:
                    WhereLogic.append("END")
    #--Process Where List
    try:
        dbdata = ReadFile(os.path.split(os.path.abspath(__file__))[0] + "/DB/" + tablename)
    except:
        return "Error: No this table!"
    dbdata = dbdata.split("\n")
    dbdata = [line for line in dbdata if line.strip()]
    Columns = dbdata[0].split(",")
    SetColumn = set.split("=")[0]
    SetValue = set.split("=")[1]
    VIndex = FindColumnIndex(SetColumn, dbdata[0].split(","))
    if VIndex == -1:
        return "Error: In SET no this column!!"
    count = 0
    for i in range(1, len(dbdata)):
        EachData = dbdata[i].split(",")
        if len(EachData) == len(dbdata[0].split(",")):
            if not len(WhereLogic) == 0:
                whereresult = ProcessWhereList(WhereConditionList, WhereLogic, Columns, dbdata[i])
                if (not (type(whereresult) is bool)):
                    return whereresult
                if whereresult:
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
    WriteFileArray(os.path.split(os.path.abspath(__file__))[0] + "/DB/" + tablename, dbdata)
    return str(count) + " Row(s) Updated"


def DeleteData(tablename, wherelist):
    WhereConditionList = []
    WhereLogic = []
    #Process Where List
    if (wherelist != 0):
        for i in range(len(wherelist)):
            if ("=" in wherelist[i]):
                WhereConditionList.append(wherelist[i])
                if (i + 1 < len(wherelist)):
                    WhereLogic.append(wherelist[i + 1].upper())
                else:
                    WhereLogic.append("END")
    #--Process Where List
    try:
        dbdata = ReadFile(os.path.split(os.path.abspath(__file__))[0] + "/DB/" + tablename)
    except:
        return "Error: No this table!"
    dbdata = dbdata.split("\n")
    dbdata = [line for line in dbdata if line.strip()]
    count = 0
    Columns = dbdata[0].split(",")
    for i in range(len(dbdata)):
        whereresult = ProcessWhereList(WhereConditionList, WhereLogic, Columns, dbdata[i])
        if (not (type(whereresult) is bool)):
            return whereresult
        if whereresult:
            count += 1
            dbdata[i] = ""

    DeleteEmptyLine(os.path.split(os.path.abspath(__file__))[0] + "/DB/" + tablename, dbdata)
    return "Deleted " + str(count) + " Row(s)"


def DeleteEmptyLine(filename, content):
    WriteFile(filename, "")
    file_object = codecs.open(filename, 'a', "utf-8")
    for i in range(len(content)):
        if content[i] != "":
            file_object.write(content[i] + "\n")
    file_object.close()


def WriteFileArray(filename, content):
    WriteFile(filename, "")
    file_object = codecs.open(filename, 'a', "utf-8")
    for i in range(len(content)):
        file_object.write(content[i] + "\n")
    file_object.close()


def CreateTable(name, colunm):
    if os.path.exists(os.path.split(os.path.abspath(__file__))[0] + "/DB/" + name):
        return "Error: Table already existed!"

    else:
        WriteFileLine(os.path.split(os.path.abspath(__file__))[0] + "/DB/" + name, colunm + "\n")
    return "Table " + name + " Created!"


def DropTable(name):
    if not os.path.exists(os.path.split(os.path.abspath(__file__))[0] + "/DB/" + name):
        return "Error: Table not existed!"

    else:
        os.remove(os.path.split(os.path.abspath(__file__))[0] + "/DB/" + name)
        return "Table " + name + " Droped!"


def Insert(tablename, data):
    try:
        dbdata = ReadFile(os.path.split(os.path.abspath(__file__))[0] + "/DB/" + tablename)
    except:
        return "Error: No this table!"
    dbdata = dbdata.split("\n")
    colunms = dbdata[0].split(",")
    incomingdata = data.split(",")
    if len(incomingdata) != len(colunms):
        return "Error: Length of your input VALUES and table colunms not match!"

    else:
        WriteFileLine(os.path.split(os.path.abspath(__file__))[0] + "/DB/" + tablename, data[1:-1] + "\n")
        return "A row Inserted"


def Select(tablename, selectcolumn, wherelist):
    WhereConditionList = []
    WhereLogic = []
    orderby = None
    OrderByDESC = False
    #Process Where List
    if (wherelist != 0):
        for i in range(len(wherelist)):
            if ("=" in wherelist[i]):
                WhereConditionList.append(wherelist[i])
                if (i + 1 < len(wherelist)):
                    WhereLogic.append(wherelist[i + 1].upper())
                else:
                    WhereLogic.append("END")
            elif (wherelist[i].upper() == "ORDER"):
                wherelist[i] = "ORDER"  #Make it captial, easy to process in the end of this function(process orderby)
                try:
                    if (wherelist[i + 1].upper() == "BY"):
                        wherelist[i + 1] = "BY"  #same as upper
                        orderby = wherelist[i + 2]
                    else:
                        return -1
                except:
                    return -1  #SQL Command Format Error(wherelist out of range)
            elif (wherelist[i].upper() == "DESC"):
                OrderByDESC = True
    #--Process Where List

    try:
        AllData = ReadFile(os.path.split(os.path.abspath(__file__))[0] + "/DB/" + tablename).split("\n")
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
            if len(WhereLogic) == 0:
                ReturnDatas += AllData[i].replace(",", "\t") + "\n"
            else:
                whereresult = ProcessWhereList(WhereConditionList, WhereLogic, Columns, AllData[i])
                if (not (type(whereresult) is bool)):
                    return whereresult
                if whereresult:
                    ReturnDatas += AllData[i].replace(",", "\t") + "\n"

        else:
            SingleLineData = AllData[i].split(",")
            if len(WhereLogic) == 0:
                for j in range(len(SingleLineData)):
                    if Columns[j] in selectcolumn:
                        ReturnDatas += SingleLineData[j] + "\t"
                ReturnDatas += "\n"
            else:
                if ProcessWhereList(WhereConditionList, WhereLogic, Columns, AllData[i]):
                    for j in range(len(SingleLineData)):
                        if Columns[j] in selectcolumn:
                            ReturnDatas += SingleLineData[j] + "\t"
                    ReturnDatas += "\n"

    if (orderby != None):
        Columns = ReturnDatas.split("\n")[0].split("\t")
        OrderByColumnIndex = FindColumnIndex(orderby, Columns)
        if (OrderByColumnIndex == -1):
            return "Error: In ORDER BY no this column!!"
        wherelist = [line for line in wherelist if line.strip("ORDER")]
        wherelist = [line for line in wherelist if line.strip("BY")]
        OrderbyData = Select(tablename, orderby, wherelist).split("\n")[1:]  #Remove the first column line
        OrderbyData = [line for line in OrderbyData if line.strip()]  #Remove Empty Lines
        OtherData = ReturnDatas.split("\n")[1:]
        orderdict = {}
        for i in range(len(OrderbyData)):
            try:
                orderdict[int(OrderbyData[i].strip("\t"))] = OtherData[i]
            except:
                return "Error: ORDER BY must be a number!!"
        ReturnDatas = ReturnDatas.split("\n")[0] + "\n"
        for i in sorted(orderdict, reverse=OrderByDESC):
            ReturnDatas += orderdict[i] + "\n"
    return ReturnDatas


def ProcessWhereList(WhereConditionList, WhereLogic, Columns, AllDataSingleLine):
    LegelList = []
    CIndexList = []
    for j in range(len(WhereConditionList)):
        WhereColumn = WhereConditionList[j].split("=")[0]
        WhereValue = WhereConditionList[j].split("=")[1]
        CIndex = FindColumnIndex(WhereColumn, Columns)
        if CIndex == -1:
            return "Error: In WHERE no this column!!"
        CIndexList.append(CIndex)

    EachData = AllDataSingleLine.split(",")
    if len(EachData) == len(Columns):
        #Build Legel List
        for k in range(len(WhereConditionList)):
            WhereColumn = WhereConditionList[k].split("=")[0]
            WhereValue = WhereConditionList[k].split("=")[1]
            if EachData[CIndexList[k]] == WhereValue:
                LegelList.append(True)
            else:
                LegelList.append(False)
        #--Build Legel List
        #Compute Legel List
        LastBool = False
        if (WhereLogic[0] == "AND"):
            LastBool = LegelList[0] and LegelList[1]
        elif (WhereLogic[0] == "OR"):
            LastBool = LegelList[0] or LegelList[1]
        elif (WhereLogic[0] == "END"):
            LastBool = LegelList[0]
        for k in range(len(LegelList)):
            if k <= 1:
                continue
            if (WhereLogic[k - 1] == "AND"):
                LastBool = LastBool and LegelList[k]
            elif (WhereLogic[k - 1] == "OR"):
                LastBool = LastBool or LegelList[k]
        #--Compute Legel List
        return LastBool


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
    return all_the_text


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
    file_object.write(content)
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
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_port = (IP, port)
    server.bind(ip_port)
    server.listen(5)
    sthread = threading.Thread(target=SocketBind, args=(server, ))
    sthread.setDaemon(True)
    sthread.start()
    print("TCP Socket Server Started !")
    print("Bind at " + IP + ":" + str(port))


def SocketBind(ss):
    while True:
        conn, addr = ss.accept()
        latestconn = conn
        recvsthread = threading.Thread(target=SocketReceiving, args=(conn, ))
        recvsthread.setDaemon(True)
        recvsthread.start()


def SocketReceiving(incomingconn):
    try:
        while True:
            data = incomingconn.recv(1024)
            if lock.acquire():
                result = Command(data.decode('utf-8'))
                lock.release()
            if result == -1:
                incomingconn.send("SQLike Command Format Error!".encode('utf-8'))
            else:
                incomingconn.send(str(result).encode('utf-8'))
    except:
        pass


if __name__ == '__main__':

    if (sys.version_info.major < 3):
        print("!!!WARNING!!! Please use Python3 to run SQLike. No longer support Python2 anymore!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Welcome To SQLike 0.001 Alpha")
    print("Enter \"QUIT\" or \"EXIT\" To Exit This Program")
    print("Enter \"HELP\" to show help")

    if (len(sys.argv) == 4):
        if (sys.argv[1] == "server"):
            StartSocketServer(sys.argv[2], int(sys.argv[3]))
    while 1:
        cmd = input("SQLike>>> ")
        cmd = str(cmd)
        if cmd.lower() == "quit" or cmd.lower() == "exit":
            exit(0)
        elif cmd == "":
            pass
        elif cmd.lower() == "help":
            print("Command Usage:")
            print("")
            print("1 Create table:")
            print("  CREATE TABLE _table_name (_column1,_column2,_column3....)")
            print("")
            print("2 Delete a table:")
            print("  DROP TABLE _table_name")
            print("")
            print("3 Insert a row:")
            print("  INSERT INTO _table_name VALUES (_data1,data2,_data3....)")
            print("")
            print("4 Update data without condition, means update all the data in the column:")
            print("  UPDATE _table_name SET _column=_data")
            print("")
            print("5 Update data with condition:")
            print("  UPDATE _table_name SET _column=_data WHERE _column=_data")
            print("")
            print("6 Delete a row:")
            print("  DELETE FROM _table_name WHERE _column=_data")
            print("")
            print("7 Query all the data with all columns:")
            print("  SELECT * FROM _table_name")
            print("")
            print("8 Query some data with all columns with a special condition:")
            print("  SELECT * FROM _table_name WHERE _column=_data")
            print("")
            print("9 Query all the data only with special column(s):")
            print("  SELECT _column1,_column2 FROM _table_name")
            print("")
            print("10 Query some data only with special single column with a special condition:")
            print("  SELECT _column1,_column2 FROM _table_name WHERE _column=_data")
            print("")
            print("11 Query data and sort (Just add ORDER BY at the end of all kind of SELECT command) eg:")
            print("  SELECT _column1,_column2 FROM _table_name WHERE _column=_data ORDER BY _column1")
            print("  (Note: ORDER BY must be a number)")
            print("")
            print("12 Sort in descending order (Just add DESC after ORDER BY _column) eg:")
            print("  SELECT * FROM _table_name ORDER BY _column1 DESC")
            print("")
            print("13 Start TCP Socket Server")
            print("  server BindIP:PORT")
            print("  Example: server 0.0.0.0:1666")
            print("")
        elif cmd.split(" ")[0].lower() == "server":
            if len(cmd.split(" ")) == 2:
                if len(cmd.split(" ")[1].split(":")) == 2:
                    StartSocketServer(cmd.split(" ")[1].split(":")[0], int(cmd.split(" ")[1].split(":")[1]))
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
                    print(cmdResult)
                lock.release()
