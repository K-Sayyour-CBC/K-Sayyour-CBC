import pyodbc


#Get The Data In The 2 Given Tables
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

#Merge The 2 Given Tables Based On The Given Key Column
def MergeTables(SourceTable, TargetTable, KeyColumn):
    try:
        Values = "("
        Set = ""
        Schema = (list(zip(*GetSchema(TargetTable)))[0])
        #Values
        for i in Schema:
            Values = Values + " Source."+str(i)+","
        Values = Values[:-1:]
        Values = Values +")"

        for i in Schema:
            Set = Set + "Target."+str(i)+" = Source."+str(i)+",\n"
        Set = Set[:-2:]
        Set = Set +";"
        #MergeStatement
        MergeStatement = "MERGE "+TargetTable+" AS Target\nUSING "+SourceTable+" AS Source\nON Source."+KeyColumn+" = Target."+KeyColumn+"\nWHEN NOT MATCHED BY Target THEN\n  INSERT ("
        for i in Schema:
            MergeStatement = MergeStatement+str(i)+", "
        MergeStatement = MergeStatement[:-2:]
        MergeStatement = MergeStatement +")\n  VALUES "+str(Values)+"\nWHEN MATCHED THEN \nUPDATE \nSET \n   "+str(Set)

        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-60R3M68\LOCALHOST;DATABASE=SSISTutorials;Trusted_Connection=yes;')  
        cursor = conn.cursor()
        cursor.execute(MergeStatement)
        conn.commit()

    except:
        print("Failed To Execute The Statement:")
        print(MergeStatement)
    
    else:
        print("Success! The Merge Statement:")
        print(MergeStatement)
        print("Was Successfuly Executed On the Data Base For Tables "+SourceTable+" And "+TargetTable)

    finally:
        conn.close()
    
MergeTables("CDCSource", "CDCTarget", "EmployeeID")
