IF (OBJECT_ID('Product') is not null) TRUNCATE TABLE Product 
IF OBJECT_ID('Product') is null) 
CREATE TABLE CDCHistoryProduct
(SEQ int NOT NULL
,ProductID int  primary key
,Name nvarchar (30) not null
,Category nvarchar (30) not null
,Color nvarchar (30) not null
,LoadTime datetime
,ProcessingTime datetime 
);