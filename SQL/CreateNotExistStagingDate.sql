IF (OBJECT_ID('Date') is null) 
CREATE TABLE CDCStagingDate
(SEQ int NOT NULL
,DateKey datetime  primary key
,Year int  not null
,Quarter int  not null
,Month nvarchar (30) not null
,Day int  not null
,LoadTime datetime default getdate()
);