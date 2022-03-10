import pyodbc
import CreateTableFromMetadata as CTFM

#Create The Given Table From MetaData Table And Its Corresponding Staging, Processing, History, and Target Tables
def CreateEnvironment(TableName):

    try:
        Statement = CTFM.CreateStaging(TableName)
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute(Statement)
        conn.commit()
    
    except:
        print("Failed To Create The Staging Table "+TableName)

    else:
        print("Success! The Staging Table "+TableName+" Has Been Created Successfuly!")
    
    finally:
        conn.close()

    try:
        Statement = CTFM.CreateProcessing(TableName)
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute(Statement)
        conn.commit()
    
    except:
        print("Failed To Create The Processing Table "+TableName)

    else:
        print("Success! The Processing Table"+TableName+" Has Been Created Successfuly!")
    
    finally:
        conn.close()

    try:
        Statement = CTFM.CreateHistory(TableName)
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute(Statement)
        conn.commit()
    
    except:
        print("Failed To Create The History Table "+TableName)

    else:
        print("Success! The History Table "+TableName+" Has Been Created Successfuly!")
    
    finally:
        conn.close()

    try:
        Statement = CTFM.CreateTarget(TableName)
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=IncrementalProcessing;Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute(Statement)
        conn.commit()
    
    except:
        print("Failed To Create The Target Table "+TableName)

    else:
        print("Success! The Target Table "+TableName+" Has Been Created Successfuly!")
    
    finally:
        conn.close()





#CreateEnvironment("Employee")
CreateEnvironment("Customer")
CreateEnvironment("Product")
CreateEnvironment("Date")
CreateEnvironment("Order")




