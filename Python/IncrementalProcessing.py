import pyodbc


#Create File "SQLFile" And Write The SQL_Statement In The File
def CreateFile(FileName, SQLStatement):
    try:
        f = open(FileName, "w")
        f.write(SQLStatement)
        
    except:
        print("Failed To Create\Open File "+FileName)
        print("Failed To Write "+SQLStatement+" To File "+FileName)
    else:
        print("Success! The SQL Statement \n"+SQLStatement+"Was Written To File "+FileName)
    finally:
        f.close()

#Get Schema Function
def GetSchema(table):
    try:
        smcol = []      
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute("select column_name from information_schema.columns where table_schema = 'dbo' and table_name = '"+table+"'")
        Values = cursor.fetchall()
        for i in Values:
            smcol.append(i[0])
        
    except:
        print("Failed To Connect To Data Base")
        print("Failed To Execute Query To Get "+table+" Schema")
    
    else:       
        print("Success! The Schema Columns List Of "+table+" Is: ")
        print(smcol)
        return smcol
    finally:
        conn.close()

#Get Data Function
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
#Sort Data Based On The # Given Key Columns
def SortData(TableName, FirstKey, SecondKey, ThirdKey):
    try:
        Schema = GetSchema(TableName)
        FKey = Schema.index(FirstKey)
        SKey = Schema.index(SecondKey)
        ThKey = Schema.index(ThirdKey)

        Data = GetData(TableName)

        
        list_length = len(Data)  
        for i in range(0, list_length):  
            for j in range(0, list_length-i-1):
                ith = FKey 
                if (Data[j][ith] > Data[j + 1][ith]):  
                    temp = Data[j]  
                    Data[j]= Data[j + 1]  
                    Data[j + 1]= temp 

                elif (Data[j][ith] == Data[j + 1][ith]):
                    ith = SKey
                    if (Data[j][ith] > Data[j + 1][ith]):
                        temp = Data[j]  
                        Data[j]= Data[j + 1]  
                        Data[j + 1]= temp
                    elif (Data[j][ith] == Data[j + 1][ith]):
                        ith = ThKey
                        if (Data[j][ith] < Data[j + 1][ith]):
                            temp = Data[j]  
                            Data[j]= Data[j + 1]  
                            Data[j + 1]= temp

    except:
        print("Failed To Sort The Data")

    else:
        print("Success!")
        print(Data)
        return(Data)


#SortedData = SortData("CDCStaging", "DateInserted", "ProductID", "SEQ")
#print(SortedData)

#Create Table And Insert Data

#Create The Processing Table
def CreateProcessingTable():
    try:       
        SQLStatement = "IF (OBJECT_ID('CDCProcessing') is not null) DROP TABLE CDCProcessing CREATE TABLE CDCProcessing   (SEQ int not null, ProductID int not null ,ProductName nvarchar(255) not null  ,Category nvarchar(255) not null  ,Color nvarchar(255) not null  ,DateInserted bigint not null  ,ProcessingTime datetime default getdate());"
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute(SQLStatement)
        conn.commit()
    
    except:
        print("Failed To Create The Processing Table")

    else:
        print("Success! The Processing Table Has Been Created Successfuly!")
    
    finally:
        conn.close()
#CreateHistoryTable()


#Load The Data From Staging To Processing That Has The Same Minimum TimeStamp
def LoadData():
    try:
        Schema = GetSchema("CDCStaging")
        DateKey = Schema.index("DateInserted")
        Data = SortData("CDCStaging", "DateInserted", "ProductID", "SEQ")
        
        Part = []
        for i in Data:
            FirstDate = Data[0][DateKey]
            if i[DateKey] == FirstDate:
                Part.append(i)
        InsertStatement = "INSERT INTO CDCProcessing ([SEQ], [ProductID], [ProductName], [Category], [Color], [DateInserted]) VALUES "   
        for i in Part:
            InsertStatement = InsertStatement+str(i)+",\n"
        InsertStatement = InsertStatement[:-2:]
        InsertStatement = InsertStatement+";"
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute(InsertStatement)
        conn.commit()

    except:
        print("Failed")
    
    else:
        print("Success!")
        return Data


#Create Processed Table
def CreateProcessedTable():
    try:       
        SQLStatement = "IF (OBJECT_ID('CDCProcessed') is not null) DROP TABLE CDCProcessed CREATE TABLE CDCProcessed   (SEQ int not null, ProductID int not null ,ProductName nvarchar(255) not null  ,Category nvarchar(255) not null  ,Color nvarchar(255) not null);"
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute(SQLStatement)
        conn.commit()
    
    except:
        print("Failed To Create The Processed Table")

    else:
        print("Success! The Processed Table Has Been Created Successfuly!")
    
    finally:
        conn.close()
#CreateProcessedTable()

#Create History Table
def CreateHistoryTable():
    try:       
        SQLStatement = "IF (OBJECT_ID('CDCHistory') is not null) DROP TABLE CDCHistory CREATE TABLE CDCHistory   (SEQ int not null, ProductID int not null ,ProductName nvarchar(255) not null  ,Category nvarchar(255) not null  ,Color nvarchar(255) not null  ,DateInserted bigint not null  ,ProcessingTime datetime not null);"
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute(SQLStatement)
        conn.commit()
    
    except:
        print("Failed To Create The History Table")

    else:
        print("Success! The Processing Table Has Been Created Successfuly!")
    
    finally:
        conn.close()
#CreateHistoryTable()

#Move Data From Processing To Processed And To History
def StartTransaction(ProcessingTable):
    Data = GetData(ProcessingTable)
    History = []
    try:
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
    except:
        pass




#--------------------------SQL----------------------------------------

#Move Data With Least Time Stamp From The Specified FromTable Into The Specified IntoTable

def LeastTimeTransaction(StagingTable, ProcessingTable):
    
    IntoSchema = GetSchema(ProcessingTable)
    IntoSchema.pop(-1)
    SQLStatement = "INSERT INTO "+ProcessingTable+" ("
    for i in IntoSchema:
        SQLStatement = SQLStatement+i+", "
    SQLStatement = SQLStatement[:-2:]
    SQLStatement = SQLStatement+")\nSELECT * FROM "+StagingTable+"\nWHERE LoadTime = (SELECT min(LoadTime) FROM "+StagingTable+");\nDELETE FROM "+StagingTable+"\nWHERE LoadTime = (SELECT min(LoadTime) FROM "+StagingTable+");"
    try:
        CreateFile("SQL\IncrementalLoad\LeastTimeTransact.sql", SQLStatement)
        #conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        #cursor = conn.cursor()
        #cursor.execute(SQLStatement)
        #conn.commit()
    except:
        #conn.rollback()
        print("Failed To Do Transaction From "+StagingTable+" Into "+ProcessingTable)
    else:
        print("Success!")
        print("Transaction From "+StagingTable+" Into "+ProcessingTable+" Was Completed")
    #finally:
        #conn.close()


#Move Unwanted Data To CDCHistory
def LoadToHistory(ProcessingTable, HistoryTable):
    ProcessingSchema = GetSchema(ProcessingTable)
    SQLStatement = "INSERT INTO "+HistoryTable+" ("
    for i in ProcessingSchema:
        SQLStatement = SQLStatement+i+", "
    SQLStatement = SQLStatement[:-2:]
    SQLStatement = SQLStatement+")\nSELECT * FROM "+ProcessingTable+"\nEXCEPT\nSELECT Q.MAXSEQ AS SEQ, "
    ProcessingSchema.remove("SEQ")
    for i in ProcessingSchema:
        SQLStatement = SQLStatement+"P."+i+", "
    SQLStatement = SQLStatement[:-2:]
    SQLStatement = SQLStatement+"\nFROM "+ProcessingTable+" AS P INNER JOIN (SELECT MAX(SEQ) AS MAXSEQ, ProductID AS QProductID FROM "+ProcessingTable+" GROUP BY ProductID) AS Q\nON Q.MAXSEQ = P.SEQ AND QProductID = P.ProductID\nDELETE "+ProcessingTable+"\nFROM "+ProcessingTable+"\nINNER JOIN "+HistoryTable+" ON "+ProcessingTable+".ProductID = "+HistoryTable+".ProductID AND "+ProcessingTable+".SEQ = "+HistoryTable+".SEQ"
    try:
        CreateFile("SQL\IncrementalLoad\LoadToHistory.sql", SQLStatement)
        #conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        #cursor = conn.cursor()
        #cursor.execute(SQLStatement)
        #conn.commit()
    except:
        #conn.rollback()
        print("Failed To Do Transaction From "+ProcessingTable+" Into "+HistoryTable)
    else:
        print("Success!")
        print("Transaction From "+ProcessingTable+" Into "+HistoryTable+" Was Completed")
    #finally:
        #conn.close()


#Merge The Processing Table(SOURCE) With The Target Table(TARGET)
def MergeTables(SourceTable, TargetTable, KeyColumn):
    try:
        TargetSchema = GetSchema(TargetTable)
        #MergeStatement
        MergeStatement = "MERGE "+TargetTable+" AS Target\nUSING "+SourceTable+" AS Source\nON Source."+KeyColumn+" = Target."+KeyColumn+"\nWHEN NOT MATCHED BY Target THEN\n  INSERT ("
        for i in TargetSchema:
            MergeStatement = MergeStatement+i+", "
        MergeStatement = MergeStatement[:-2:]
        MergeStatement = MergeStatement+")\n  VALUES ("
        for i in TargetSchema:
            MergeStatement = MergeStatement+"Source."+i+", "
        MergeStatement = MergeStatement[:-2:]
        MergeStatement = MergeStatement+")\nWHEN MATCHED THEN\nUPDATE\nSET\n  "
        for i in TargetSchema:
            MergeStatement = MergeStatement+"Target."+i+" = Source."+i+",\n  "
        MergeStatement = MergeStatement[:-4:]
        MergeStatement = MergeStatement+";"
        
        CreateFile("SQL\IncrementalLoad\MergeTables.sql", MergeStatement)
        #conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')  
        #cursor = conn.cursor()
        #cursor.execute(MergeStatement)
        #conn.commit()

    except:
        print("Failed To Execute The Statement:")
        print(MergeStatement)
    
    else:
        print("Success! The Merge Statement:")
        print(MergeStatement)
        print("Was Successfuly Executed On the Data Base For Tables "+SourceTable+" And "+TargetTable)

    #finally:
        #conn.close()

#Move The Remaining Data In Processing To History
def MoveToHistory(ProcessingTable, HistoryTable):
    HistorySchema = GetSchema(ProcessingTable)
    SQLStatement = "INSERT INTO "+HistoryTable+" ("
    for i in HistorySchema:
        SQLStatement = SQLStatement+i+", "
    SQLStatement = SQLStatement[:-2:]
    SQLStatement = SQLStatement+")\nSELECT * FROM "+ProcessingTable+"\nDELETE FROM "+ProcessingTable
    try:
        CreateFile("SQL\IncrementalLoad\MoveToHistory.sql", SQLStatement)
        #conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        #cursor = conn.cursor()
        #cursor.execute(SQLStatement)
        #conn.commit()
    except:
        #conn.rollback()
        print("Failed To Do Transaction From "+ProcessingTable+" Into "+HistoryTable)
    else:
        print("Success!")
        print("Transaction From "+ProcessingTable+" Into "+HistoryTable+" Was Completed")
    #finally:
        #conn.close()


#Do The Transaction From Staging Table To Processing Table And Then To Target And History
def ProcessingTransact(StagingTable, ProcessingTable, HistoryTable, TargetTable, KeyColumn):
    try:
        LeastTimeTransaction(StagingTable, ProcessingTable)
        LoadToHistory(ProcessingTable, HistoryTable)
        MergeTables(ProcessingTable, TargetTable, KeyColumn)
        MoveToHistory(ProcessingTable, HistoryTable)
    except:
        print("Failed To Do Tarnsation")
    else:
        print("Success!")
        print("Taransaction Completed")


LeastTimeTransaction("CDCStaging", "CDCProcessing")
LoadToHistory("CDCProcessing", "CDCHistory")
MergeTables("CDCProcessing", "CDCTarget", "ProductID")
MoveToHistory("CDCProcessing", "CDCHistory")
#ProcessingTransact("CDCStaging", "CDCProcessing", "CDCProcessed", "CDCHistory", "CDCTarget", "ProductID")





