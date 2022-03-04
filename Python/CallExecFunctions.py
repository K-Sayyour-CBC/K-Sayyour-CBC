import BuiltFunctions as BF
import pyodbc
import os


#Return The Table Schema AS List
Schema1 = BF.GetSchema("table1")
Schema2 = BF.GetSchema("table2")
Schema3 = BF.GetSchema("table3")


#Return A Dictionary Containing The Corresponding Values For The Table Schema
Dictionary1 = {}
Dictionary1 = BF.GetValues(Schema1, "tableText", "Name", "Text")

Dictionary2 = {}
Dictionary2 = BF.GetValues(Schema2, "tableText", "Name", "Text")

Dictionary3 = {}
Dictionary3 = BF.GetValues(Schema3, "tableText", "Name", "Text")


#Create The SQLStatement From The Corresponding Schema And Values From Dictionary
SQLStatement1 = BF.CreateViewStatement("View1", Dictionary1, "table1")
SQLStatement2 = BF.CreateViewStatement("View2", Dictionary2, "table2")
SQLStatement3 = BF.CreateViewStatement("View3", Dictionary3, "table3")


#Create File and Write The Statements In The File
SQLStatement = SQLStatement1+";\n"+SQLStatement2+";\n"+SQLStatement3+";\n"
BF.CreateFile("SQL\SQLFile.sql", SQLStatement)


#Open And Read "SQLFile" Into SQL_String
SQLString = BF.ReadFile("SQLFile.sql")


#Execute The Query "SQL_String"
BF.ExecQuery(SQLString)


