import pyodbc
import os


#Return The List Of Schema Columns For The Given Table
def GetSchema(table): 
    try:
        smcol = []      
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=dbTest;Trusted_Connection=yes;')
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


#Get The Values of Name & Text Columns In The Table And Appened Them To 2 Given Lists Respectively
def GetValues(Schema,Table, Name, Text):
    try:
        Values = {}
        Schema = tuple(Schema)
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=dbTest;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute("SELECT "+Name+", "+Text+" FROM "+Table+" Where "+Name+" IN "+str(Schema))
        Values = cursor.fetchall()
    except:
        print("Failed To Execute The Statement And Get The Values For The Corresponding Schema")
    else:
        print("Success! The Corresponding Values For Schema Is:")
        print(Values)
        return Values
    

#Return The Create View SQL Statement Having Schema From 2 Lists And Values From Table
def CreateViewStatement(vName, Values, Table):
    try:
        SQLStatement = "CREATE VIEW dbo."+vName+" AS SELECT "
        for i in Values:
            SQLStatement = SQLStatement + str(i[0]) +" AS "
            SQLStatement = SQLStatement + str(i[1]) +", "
        SQLStatement = SQLStatement[:-2:]
        SQLStatement =SQLStatement + " FROM dbo."+Table
    except:
        print("Failed To Create The SQL Statement!")
    else:
        print("Success! The SQL Statement Has Been Successfuly Created And It Is: ")
        print(SQLStatement)
        return SQLStatement


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


#Open And Read "SQLFile" Into SQLString
def ReadFile(FileName):
    try:
        f = open(FileName, 'r')
        SQLString = f.read()

    except:
        print("Failed To Open The File "+FileName)  
        print("Failed To Read The Statement In File "+FileName)    
      
    else:
        print("Success! The SQL Statement Was Successfuly Read From File "+FileName+" and It Is: ")
        print(SQLString)
        return SQLString
    finally:
        f.close()

       
#Execute SQL_String Into The Data Base
def ExecQuery(SQLString):
    try:
        Statements = SQLString.split(";", -1)
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=dbTest;Trusted_Connection=yes;')
        cursor = conn.cursor()
        for i in Statements:
            cursor.execute(i)
            conn.commit()
    
    except:
        print("Failed To Connect To Data Base")
        print("Failed To Execute Query")
        print(SQLString)
        
    else:
        print("Successfuly Executed "+SQLString)
    finally:    
            conn.close()
