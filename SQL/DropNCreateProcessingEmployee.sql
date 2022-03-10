IF (OBJECT_ID('Employee') is not null DROP TABLE Employee 
CREATE TABLE CDCProcessingEmployee
(SEQ int NOT NULL
,EmployeeID int  primary key
,Name nvarchar (30) not null
,Title nvarchar (30) not null
,Country nvarchar (30) not null
,Salary Float  not null
,LoadTime datetime
,ProcessingTime datetime default getdate()
);