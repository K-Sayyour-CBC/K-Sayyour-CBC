import pyodbc
import IncrementalProcessing as IP



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


def CreateProcedure(TableName, KeyColumn):
    try: 
        Procedure = "IF (object_id('usp_"+TableName+"') is not null) DROP PROCEDURE usp_"+TableName+";\nGO\nCREATE\nPROCEDURE usp_"+TableName+"\nAS\nBEGIN\n  BEGIN TRY\n  "
        Statement = IP.LeastTimeTransaction(TableName)
        Procedure = Procedure + Statement
        Procedure = Procedure + "  END TRY\n  BEGIN CATCH\n    ROLLBACK TRAN;\n  END CATCH\n  BEGIN TRY\n  "
        Statement = IP.LoadToHistory(TableName, KeyColumn)
        Procedure = Procedure + Statement
        Procedure = Procedure + "  END TRY\n  BEGIN CATCH\n    ROLLBACK TRAN;\n  END CATCH\n  BEGIN TRY\n  BEGIN TRANSACTION;\n"
        Statement = IP.MergeTables(TableName, KeyColumn)
        Procedure = Procedure + Statement
        Procedure = Procedure + "END TRY\n  BEGIN CATCH\n    ROLLBACK TRAN;\n  END CATCH\n  BEGIN TRY\n "   
        Statement = IP.MoveToHistory(TableName)
        Procedure = Procedure + Statement
        Procedure = Procedure + "END TRY\n  BEGIN CATCH\n    ROLLBACK TRAN;\n   END CATCH\nEND;"   
      
    except:
        print("Failed To Create The Procedure usp_"+TableName)
    
    else:
        print("Success! The Procedure Statement Was Created")
        CreateFile ("usp_"+TableName+".sql", Procedure)
        return Procedure
    
def ExecuteProcedure(TableName):
    try:
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute("EXEC usp_"+TableName)
        conn.commit()

    except:
        print("Failed To Execute The Procedure")
    
    else:
        print("Success! The Procedure Was Executed")




#CreateProcedure("Product", "ProductID")
#ExecuteProcedure("Product")

CreateProcedure("Employee", "EmployeeID")
#ExecuteProcedure("Employee")

CreateProcedure("Customer", "CustomerID")
#ExecuteProcedure("Customer")

CreateProcedure("Date", "DateKey")
#ExecuteProcedure("Date")

CreateProcedure("Order", "OrderID")
#ExecuteProcedure("Order")