import pyodbc


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
print(Set)"""
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






"""Statement = "CREATE TABLE table1 \n("
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
        j = j + 1"""



    
