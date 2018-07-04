import codecs
import os


def Command(cmd):
    c = cmd.split(" ")
    if c[0] == "CREATE" and c[1] == "TABLE":
        CreateTable(c[2], c[3][1:-1])
    elif c[0] == "DROP" and c[1] == "TABLE":
        DropTable(cmd.split(" ")[2])
    elif c[0] == "INSERT" and c[1] == "INTO" and c[3] == "VALUES":
        Insert(c[2], c[4])
    elif c[0] == "SELECT" and c[2] == "FROM":
        if (len(c) > 5):
            Select(c[3], c[1], c[5])
        else:
            Select(c[3], c[1], 0)
    elif c[0] == "DELETE" and c[1] == "FROM" and c[3] == "WHERE":
        DeleteData(c[2], c[4])
    elif c[0] == "UPDATE" and c[2] == "SET":
        if (len(c) > 5):
            UpdateData(c[1], c[3], c[5])
        else:
            UpdateData(c[1], c[3], 0)

    else:
        print "Command Format Error!"


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
                    UpdateLine("DB/" + tablename, i, newData)
            else:
                EachData[VIndex] = SetValue
                newData = ""
                for j in range(len(EachData)):
                    newData += EachData[j] + ","
                newData = newData[:-1]
                UpdateLine("DB/" + tablename, i, newData)


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
                DeleteLine("DB/" + tablename, i)


def UpdateLine(filename, line, content):
    file_object = open(filename)
    all_the_text = file_object.read()
    file_object.close()
    lines = all_the_text.split("\n", )
    lines[line] = content
    WriteFile(filename, "")
    for i in range(len(lines)):
        if lines[i] != "":
            WriteFileLine(filename, unicode(lines[i]) + "\n")


def DeleteLine(filename, line):
    file_object = open(filename)
    all_the_text = file_object.read()
    file_object.close()
    lines = all_the_text.split("\n", )
    lines[line] = ""
    WriteFile(filename, "")
    for i in range(len(lines)):
        if lines[i] != "":
            WriteFileLine(filename, unicode(lines[i]) + "\n")


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
    for i in range(len(AllData)):
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
    print "Welcome To SQLike 0.0001 Alpha Command Tool"
    print "Enter quit Or exit To Exit This Program"
    while 1:
        cmd = raw_input("SQLike>>> ")
        cmd = str(cmd)
        if cmd == "quit" or cmd == "exit":
            exit(0)
        elif cmd  == "":
			pass
        else:
            Command(cmd)
