import codecs
import os


def Command(cmd):
    try:
        c = cmd.split(" ")
        if c[0] == "CREATE" and c[1] == "TABLE":
            if not len(c) == 4:
                return -1
            if not c[3][0] == "(":
                return -1
            if not c[3][-1] == ")":
                return -1
            CreateTable(c[2], c[3][1:-1])
        elif c[0] == "DROP" and c[1] == "TABLE":
            if not len(c) == 3:
                return -1
            DropTable(c[2])
        elif c[0] == "INSERT" and c[1] == "INTO" and c[3] == "VALUES":
            if not len(c) == 5:
                return -1
            if not c[4][0] == "(":
                return -1
            if not c[4][-1] == ")":
                return -1
            Insert(c[2], c[4])
        elif c[0] == "SELECT" and c[2] == "FROM":
            if len(c) == 6:
                if not len(c[5].split("=")) == 2:
                    return -1
                Select(c[3], c[1], c[5])
            elif len(c) == 4:
                Select(c[3], c[1], 0)
            else:
                return -1

        elif c[0] == "DELETE" and c[1] == "FROM" and c[3] == "WHERE":
            if not len(c) == 5:
                return -1
            if not len(c[4].split("=")) == 2:
                return -1
            DeleteData(c[2], c[4])
        elif c[0] == "UPDATE" and c[2] == "SET":
            if not len(c[3].split("=")) == 2:
                return -1
            if len(c) == 6:
                if not len(c[5].split("=")) == 2:
                    return -1
                UpdateData(c[1], c[3], c[5])
            else:
                UpdateData(c[1], c[3], 0)

        else:
            return -1
    except:
        return -1


def UpdateData(tablename, set, where):
    dbdata = ReadFile("DB/" + tablename)
    dbdata = dbdata.split("\n")
    SetColumn = set.split("=")[0]
    SetValue = set.split("=")[1]
    VIndex = FindColumnIndex(SetColumn, dbdata[0].split(","))
    if VIndex == -1:
        print("Error: In SET no this column!!")
        return
    for i in range(1, len(dbdata)):
        EachData = dbdata[i].split(",")
        if len(EachData) == len(dbdata[0].split(",")):
            if not where == 0:
                WhereColumn = where.split("=")[0]
                WhereValue = where.split("=")[1]
                CIndex = FindColumnIndex(WhereColumn, dbdata[0].split(","))
                if CIndex == -1:
                    print("Error: In WHERE no this column!!")
                    return
                if EachData[CIndex] == WhereValue:
                    EachData[VIndex] = SetValue
                    newData = ""
                    for j in range(len(EachData)):
                        newData += EachData[j] + ","
                    newData = newData[0:-1]
                    dbdata[i] = newData
                    # UpdateLine("DB/" + tablename, i, newData)
            else:
                EachData[VIndex] = SetValue
                newData = ""
                for j in range(len(EachData)):
                    newData += EachData[j] + ","
                newData = newData[0:-1]
                dbdata[i] = newData
                # UpdateLine("DB/" + tablename, i, newData)
    WriteFileArray("DB/" + tablename, dbdata)


def DeleteData(tablename, where):
    dbdata = ReadFile("DB/" + tablename)
    dbdata = dbdata.split("\n")
    WhereColumn = where.split("=")[0]
    WhereValue = where.split("=")[1]
    CIndex = FindColumnIndex(WhereColumn, dbdata[0].split(","))
    if CIndex == -1:
        print("Error: In WHERE no this column!!")
        return
    for i in range(len(dbdata)):
        EachData = dbdata[i].split(",")
        if len(EachData) == len(dbdata[0].split(",")):
            if EachData[CIndex] == WhereValue:
                dbdata[i] = ""
                # DeleteLine("DB/" + tablename, i)
    DeleteEmptyLine("DB/" + tablename, dbdata)


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
    if os.path.exists("DB/" + name):
        print "Error: Table already existed!"
        return
    else:
        WriteFileLine("DB/" + name, colunm + "\n")
    print "Table " + name + " Created!"


def DropTable(name):
    if not os.path.exists("DB/" + name):
        print "Error: Table not existed!"
        return
    else:
        os.remove("DB/" + name)
        print ("Table " + name + " Droped!")


def Insert(tablename, data):
    dbdata = ReadFile("DB/" + tablename)
    dbdata = dbdata.split("\n")
    colunms = dbdata[0].split(",")
    incomingdata = data.split(",")
    if len(incomingdata) != len(colunms):
        print "Error: Length of your input VALUES and table colunms not match!"
        return
    else:
        WriteFileLine("DB/" + tablename, data[1:-1] + "\n")


def Select(tablename, selectcolumn, where):
    AllData = ReadFile("DB/" + tablename).split("\n")
    Columns = AllData[0].split(",")
    ReturnDatas = ""
    if not selectcolumn[0] == "*":
        for i in range(len(Columns)):
            if Columns[i] in selectcolumn:
                ReturnDatas += Columns[i] + " "
    else:
        for i in range(len(Columns)):
            ReturnDatas += Columns[i] + " "
    ReturnDatas += "\n"
    for i in range(1, len(AllData)):
        if selectcolumn == "*":
            if where == 0:
                ReturnDatas += AllData[i].replace(",", " ") + "\n"
            else:
                WhereColumn = where.split("=")[0]
                WhereValue = where.split("=")[1]
                CIndex = FindColumnIndex(WhereColumn, Columns)
                if CIndex == -1:
                    print("Error: In WHERE no this column!!")
                    return
                EachData = AllData[i].split(",")
                if len(EachData) == len(AllData[0].split(",")):
                    if EachData[CIndex] == WhereValue:
                        ReturnDatas += AllData[i].replace(",", " ") + "\n"
        else:
            SingleLineData = AllData[i].split(",")
            if where == 0:
                for j in range(len(SingleLineData)):
                    if Columns[j] in selectcolumn:
                        ReturnDatas += SingleLineData[j] + " "
                ReturnDatas += "\n"
            else:
                WhereColumn = where.split("=")[0]
                WhereValue = where.split("=")[1]
                CIndex = FindColumnIndex(WhereColumn, Columns)
                if CIndex == -1:
                    print("Error: In WHERE no this column!!")
                    return
                EachData = AllData[i].split(",")
                if len(EachData) == len(AllData[0].split(",")):
                    if EachData[CIndex] == WhereValue:
                        for j in range(len(SingleLineData)):
                            if Columns[j] in selectcolumn:
                                ReturnDatas += SingleLineData[j] + " "
                        ReturnDatas += "\n"
    print ReturnDatas


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


if __name__ == '__main__':
    print "Welcome To SQLike 0.0002 Alpha Command Tool"
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
            print "Create table:"
            print "CREATE TABLE _table_name (_column1,_column2,_column3....)"
            print ""
            print "Delete a table:"
            print "DROP TABLE _table_name"
            print ""
            print "Insert a row:"
            print "INSERT INTO _table_name VALUES (_data1,data2,_data3....)"
            print ""
            print "Update data without condition, means update all the data in the column:"
            print "UPDATE _table_name SET _column=_data"
            print ""
            print "Update data with condition:"
            print "UPDATE _table_name SET _column=_data WHERE _column=_data"
            print ""
            print "Delete a row:"
            print "DELETE _table_name WHERE _column=_data"
            print ""
            print "Query all the data with all columns:"
            print "SELECT * FROM _table_name"
            print ""
            print "Query some data with all columns with a special condition:"
            print "SELECT * FROM _table_name WHERE _column=_data"
            print ""
            print "Query all the data only with special single column:"
            print "SELECT _column=_data FROM _table_name"
            print ""
            print "Query some data only with special single column with a special condition:"
            print "SELECT _column=_data FROM _table_name WHERE _column=_data"
        else:
            err = Command(cmd)
            if err == -1:
                print("SQLike Command Format Error!")
