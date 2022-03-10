import pyodbc
import os

"""Values = [('Customer  ', 'Number    ', 'int       ', None, True), ('Customer  ', 'Name      ', 'nvarchar  ', '35        ', False), ('Customer  ', 'Country   ', 'nvarchar  ', '10        ', False), ('Customer  ', 'DOB       ', 'nvarchar  ', '35        ', False)]
col1 = (list(zip(*Values))[1])
col2 = (list(zip(*Values))[2])
col3 = (list(zip(*Values))[3])
col4 = (list(zip(*Values))[4])
Tuple = ("EmpID", "FName", "LName", "Education", "Occupation", "YearlyIncome", "Sales")
Values = "("
Set = ""
for i in Tuple:
    Values = Values + " Source."+i+","
Values = Values[:-1:]
Values = Values +")"
print(Values)

for i in Tuple:
    Set = Set + "Target."+i+" = Source."+i+",\n"
Set = Set[:-2:]
Set = Set +";"
print(Set)
def GetSchema(TableName):
    try:
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=SSISTutorials;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute("select column_name from information_schema.columns where table_schema = 'dbo' and table_name = '"+TableName+"'")
        Values = cursor.fetchall()
    
    except:
        print("Failed To Execute The Statement Against The Data Base")
    
    else:
        print("Success! The Schema Of "+TableName+" Is: ")
        print(Values)
        return Values
    
    finally:
        conn.close()
List = []
Schema = GetSchema("CDCTarget")
Values = (list(zip(*Schema))[0])
for i in Values:
    List.append(i)
print(List)

Statement = "CREATE TABLE table1 \n("
for i in Values:
    j = 1
    i = list(i)
    while j > 4:
        if i [j][-2] == None:
            del i [j][-2]
        if i [j][-1] == True:
            del i [j][-1]
            i.append("primary key")
        else:
            del i [j][-1]
            i.append("not null")
        Statement = Statement + (i [j][:])
        j = j + 1

#Generate SQL "CREATE" Script To File
def CreateFile(FileName, CreateTable):
    try:
        f = open(FileName, "w")
        f.write(CreateTable)

    except:
        print("Failed To Open\Create File: "+FileName)
        print("Failed To Write The Statement ")
        print(CreateTable+" To The File "+FileName)

    else:
        print("Success! The Create Statement ")
        print(CreateTable)
        print("Was Successfuly Written To The File "+FileName)

    finally:
        f.close()
    
CreateFile("SQL/CreateFile.sql", "fnbvi ujb gfvid fbnh vitjugb vdpiubnv diupnvb dijurfbs[dnhv iuasdnbj dsv")
String = "    cuhc        "
tString = String.strip()
print(tString)
print(String)"""



    
"""Data = [(0, 30, 'Zhu', 'Bachelors', 'Professional', 20220224080000), (0, 40, 'Miller', 'Masters Degree', 'Management', 20220224080000), (0, 40, 'Miller', 'Masters Degree', 'Management', 20220224080000), (1, 50, 'Verhoff', 'Partial High School', 'Clerical', 20220224080000), (1, 30, 'Zhu', 'Bachelors', 'Professional', 20220224090000), (0, 30, 'Zhu', 'Bachelors', 'Professional', 20220224090000), (0, 30, 'Zhu', 'Bachelors','Professional', 20220225080000), (1, 40, 'Miller', 'Masters Degree', 'Management', 20220225080000), (0, 40, 'Miller', 'Masters Degree', 'Management', 20220225080000), (0, 50, 'Verhoff', 'Partial High School', 'Clerical', 20220225080000), (0, 50, 'Verhoff', 'Partial High School', 'Clerical', 20220225080000), (0, 50, 'Verhoff', 'Partial High School', 'Clerical', 20220225090000), (0, 30, 'Zhu', 'Bachelors', 'Professional', 20220226080000), (0, 40, 'Miller', 'Masters Degree', 'Management', 20220226080000), (0, 50, 'Verhoff', 'Partial High School', 'Clerical', 20220226080000)]

Part = []
for i in Data:
    FirstDate = Data[0][5]
    if i[5] == FirstDate:
        Part.append(i)
InsertStatement = "INSERT INTO CDCProcessing ([SEQ], [ProductID], [ProductName], [Category], [Color], [DateInserted]) VALUES "   
for i in Part:
    InsertStatement = InsertStatement+str(i)+",\n"
InsertStatement = InsertStatement[:-2:]
InsertStatement = InsertStatement+";"
print(InsertStatement)

def GetData(TableName):
    try:
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+TableName)
        Values = cursor.fetchall()
    
    except:
        print("Failed To Execute The Statement Against The Data Base")
    
    else:
        print("Success! The Data Of "+TableName+" Is: ")
        print(Values)
        return Values




Data = [(0,30), (0,40), (0,50), (1,30), (2,30), (1,40)]
History =[]
print("Before")
print(Data)
print(History)
for i in range(0, len(Data)):
    if Data[i][0] == 0:
        for j in range(0, len(Data)):
            if Data[j][0] > Data[i][0] and Data[j][1] == Data[i][1]:
                History.append(Data[i])
        
    else:
        for j in range(0, len(Data)):
            if Data[j][0] > Data[i][0] and Data[j][1] == Data[i][1]:
                History.append(Data[i])
History = list(dict.fromkeys(History))"""



"""Data = [(0,30), (0,40), (0,50), (1,30), (2,30), (1,40)]
    History =[]
    print("Before")
    print(Data)
    print(History)
    for i in range(0, len(Data)):
        if Data[i][0] == 0:
            for j in range(0, len(Data)):
                if Data[j][0] > Data[i][0] and Data[j][1] == Data[i][1]:
                    History.append(Data[i])
        
        else:
            for j in range(0, len(Data)):
                if Data[j][0] > Data[i][0] and Data[j][1] == Data[i][1]:
                    History.append(Data[i])
    History = list(dict.fromkeys(History))



#Get Table Columns Description With Corresponding Schema From Metadata Table Into A List Of Tuples
def GetTableDescription(TableName):
    try:
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MetaData Where TableName = '"+TableName+"'")
        Values = cursor.fetchall()

    except:
        print("Failed To Execute Statement And Get The Columns Descriptions")
    
    else:
        print("Success! The Table "+TableName+" Has The Following Column Descriptions")
        print(Values)
        return Values
    
    finally:
        conn.close()

#Create Processing Table
def CreateProcessing(TableName):
    try:
        TableDescription = GetTableDescription(TableName)
        Statement = "CREATE TABLE CDCProcessing"+TableName+"\n(SEQ int NOT NULL\n,"
        col1 = (list(zip(*TableDescription))[1])
        col2 = (list(zip(*TableDescription))[2])
        col3 = (list(zip(*TableDescription))[3])
        col4 = (list(zip(*TableDescription))[4])
        print("The Columns Are:")
        print(col1, col2, col3, col4)
        j = 0
        col1 = list(col1)
        col2 = list(col2)
        col3 = list(col3)
        col4 = list(col4)
        while j < len(col1):
            if col3[j] == None:
                col3[j] = ""
                
            
            else:
                col3[j] = "("+str(col3[j])+")"

            if col4[j] == True:
                col4[j] = "primary key"

            else:
                col4[j] = "not null"   
            Statement = Statement+str(col1[j])+" "+str(col2[j])+" "+str(col3[j])+" "+str(col4[j])+"\n,"
            j = j + 1
        Statement = Statement+"LoadTime datetime\n,ProcessingTime datetime default getdate()\n);"
        
    except:
        print("Failed To Create Table Processing")
    
    else:
        print("SUCCESS!")
        return Statement


#Create History Table
def CreateHistory(TableName):
    try:
        TableDescription = GetTableDescription(TableName)
        Statement = "CREATE TABLE CDCHistory"+TableName+"\n(SEQ int NOT NULL\n,"
        col1 = (list(zip(*TableDescription))[1])
        col2 = (list(zip(*TableDescription))[2])
        col3 = (list(zip(*TableDescription))[3])
        col4 = (list(zip(*TableDescription))[4])
        print("The Columns Are:")
        print(col1, col2, col3, col4)
        j = 0
        col1 = list(col1)
        col2 = list(col2)
        col3 = list(col3)
        col4 = list(col4)
        while j < len(col1):
            if col3[j] == None:
                col3[j] = ""
                
            
            else:
                col3[j] = "("+str(col3[j])+")"

            if col4[j] == True:
                col4[j] = "primary key"

            else:
                col4[j] = "not null"   
            Statement = Statement+str(col1[j])+" "+str(col2[j])+" "+str(col3[j])+" "+str(col4[j])+"\n,"
            j = j + 1
        Statement = Statement+"LoadTime datetime\n,ProcessingTime datetime \n);"
        
    except:
        print("Failed To Create Table Processing")
    
    else:
        print("SUCCESS!")
        return Statement"""

