import pyodbc
import os

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


#Create Table Statement From The Given Descriptions
def CreateTable(TableName):
    try:
        TableDescription = GetTableDescription(TableName)
        Statement = "CREATE TABLE "+TableName+"\n("

    except:
        print("Failed To Get The Table Schema For The Table "+TableName)

    else:
        print("Success! The Table Schema Description List Is:")
        print(TableDescription)

    try:
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
        
        Statement = Statement[:-1:]+"\n);"

    except:
        print("Failed To Create The Create Statement For The Table "+TableName)
    
    else:
        print("Success! The Statment For Creating The Table "+TableName+" Is:")
        print(Statement)
        return Statement



#Create Staging Table
def CreateStaging(TableName):
    try:
        TableDescription = GetTableDescription(TableName)
        Statement = "CREATE TABLE CDCStaging"+TableName+"\n(SEQ int NOT NULL\n,"
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
        Statement = Statement+"LoadTime datetime default getdate()\n);"
        
    except:
        print("Failed To Create Table Staging")
    
    else:
        print("SUCCESS!")
        return Statement


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
        return Statement


#Create Target Table
def CreateTarget(TableName):
    try:
        TableDescription = GetTableDescription(TableName)
        Statement = "CREATE TABLE CDCTarget"+TableName+"\n("

    except:
        print("Failed To Get The Table Schema For The Table "+TableName)

    else:
        print("Success! The Table Schema Description List Is:")
        print(TableDescription)

    try:
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
        
        Statement = Statement[:-1:]+"\n);"

    except:
        print("Failed To Create The Create Statement For The Table "+TableName)
    
    else:
        print("Success! The Statment For Creating The Table "+TableName+" Is:")
        print(Statement)
        return Statement



#Generate SQL "CREATE" Script To File
def CreateFile(FileName, CreateTable):
    try:
        f = open("SQL/"+FileName, "w")
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
    


#Generate SQL "CREATE IF NOT EXIST" Script To File
def CreateNotExstFile(FileName, CreateTable, TableName):
    try:
        NotExst = "IF (OBJECT_ID('"+TableName+"') is null) \n"
        NotExstStatement = NotExst + CreateTable
        f = open("SQL/"+FileName, "w")
        f.write(NotExstStatement)

    except:
        print("Failed To Open\Create File: "+FileName)
        print("Failed To Write The Statement ")
        print(NotExstStatement+" To The File "+FileName)

    else:
        print("Success! The CREATE IF NOT EXIST Statement ")
        print(NotExstStatement)
        print("Was Successfuly Written To The File "+FileName)

    finally:
        f.close()

#Generate SQL "DROP AND CREATE" Script To File
def DropNCreateFile(FileName, CreateTable, TableName):
    try:
        Drop = "IF (OBJECT_ID('"+TableName+"') is not null DROP TABLE "+TableName+" \n"
        DropStatement = Drop + CreateTable
        f = open("SQL/"+FileName, "w")
        f.write(DropStatement)

    except:
        print("Failed To Open\Create File: "+FileName)
        print("Failed To Write The Statement ")
        print(DropStatement+" To The File "+FileName)
    
    else:
        print("Success! The DROP AND CREATE TABLE Statement ")
        print(DropStatement)
        print("Was Successfuly Written To The File "+FileName)

    finally:
        f.close()

#Generate SQL "TRUNCATE OR CREATE" Script To File
def TrunOrCreateFile(FileName, CreateTable, TableName):
    try:
        Trun = "IF (OBJECT_ID('"+TableName+"') is not null) TRUNCATE TABLE "+TableName+" \nIF OBJECT_ID('"+TableName+"') is null) \n"
        TrunStatement = Trun + CreateTable
        f = open("SQL/"+FileName, "w")
        f.write(TrunStatement)

    except:
        print("Failed To Open\Create File: "+FileName)
        print("Failed To Write The Statement ")
        print(TrunStatement+" To The File "+FileName)
    
    else:
        print("Success! The TRUNCATE OR CREATE TABLE Statement ")
        print(TrunStatement)
        print("Was Successfuly Written To The File "+FileName)

"""#Create Statments For The Given Table Name
CreateCustomer = CreateTable("Customer")
CreateStagingDate = CreateStaging("Date")
CreateProcessingEmpolyee = CreateProcessing("Employee")
CreateHistoryProduct = CreateHistory("Product")
CreateTargetOrder = CreateTarget("Order")

#Create Files That Include The Given Create Statement For Each Creation Case 
CreateFile("CreateCustomer.sql", CreateCustomer)
CreateNotExstFile("CreateNotExistStagingDate.sql", CreateStagingDate, "Date")
DropNCreateFile("DropNCreateProcessingEmployee.sql", CreateProcessingEmpolyee, "Employee")
TrunOrCreateFile("TrunOrCreateHistoryProduct.sql", CreateHistoryProduct, "Product")
CreateFile("CreateTargetSales.sql", CreateTargetOrder)"""


