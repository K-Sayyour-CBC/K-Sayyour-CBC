
-----------------CREATE MetaData TABLE--------------

IF (OBJECT_ID('MetaData') is not null) DROP TABLE MetaData
CREATE TABLE MetaData
	(TableName nvarchar(30) not null
	,FieldName nvarchar(30) not null
	,DataType1 nvarchar(30) not null
	,DataType2 nvarchar(30)
	,IsKey bit not null
	);

INSERT INTO MetaData
VALUES
('Employee', 'EmployeeID', 'int',NULL ,1),
('Employee', 'Name', 'nvarchar','30',0),
('Employee', 'Title', 'nvarchar','30',0),
('Employee', 'Country', 'nvarchar','30',0),
('Employee', 'Salary', 'Float',NULL ,0),
('Customer', 'CustomerID', 'int',NULL ,1),
('Customer', 'Name', 'nvarchar','30',0),
('Customer', 'Addresse', 'nvarchar','30',0),
('Product', 'ProductID', 'int',NULL ,1),
('Product', 'Name','nvarchar','30',0),
('Product', 'Category','nvarchar','30',0),
('Product', 'Color','nvarchar','30',0),
('Date', 'DateKey','datetime',NULL ,1),
('Date', 'Year','int',NULL ,0),
('Date', 'Quarter','int',NULL ,0),
('Date', 'Month','nvarchar','30',0),
('Date', 'Day','int',NULL ,0),
('Order', 'OrderID','int',NULL ,1),
('Order', 'ProductID','int',NULL ,0),
('Order', 'CustomerID','int',NULL ,0),
('Order', 'DateKey','int',NULL ,0),
('Order', 'Price','float',NULL ,0),
('Order', 'Quantity','int',NULL ,0);

SELECT * FROM MetaData

-----------------CREATE CDCStaging TABLE--------------


IF (OBJECT_ID('CDCStaging') is not null) DROP TABLE CDCStaging
CREATE TABLE CDCStaging
	(SEQ int not null
	,ProductID int not null
	,Name nvarchar(255) not null
	,Category nvarchar(255) not null
	,Color nvarchar(255) not null
	,LoadTime bigint not null
	);


INSERT INTO CDCStaging (SEQ, ProductID, Name, Category, Color, LoadTime)
VALUES
(0, 50, 'Verhoff', 'Partial High School', 'Clerical', 20220224080000),
(0, 40, 'Miller', 'Masters Degree', 'Management', 20220224080000),
(2, 40, 'Miller', 'Masters Degree', 'Management', 20220224080000),
(0, 30, 'Zhu', 'Bachelors', 'Professional', 20220224080000),
(1, 30, 'Zhu', 'Bachelors', 'Professional', 20220224080000),
(0, 30, 'Zhu', 'Bachelors', 'Professional', 20220224090000),
(0, 40, 'Miller', 'Masters Degree', 'Management', 20220225080000),
(0, 50, 'Verhoff', 'Partial High School', 'Clerical', 20220225080000),
(0, 40, 'Miller', 'Masters Degree', 'Management', 20220226080000),
(0, 30, 'Zhu', 'Bachelors', 'Professional', 20220226080000),
(1, 40, 'Miller', 'Masters Degree', 'Management', 20220225080000),
(0, 50, 'Verhoff', 'Partial High School', 'Clerical', 20220225090000),
(0, 30, 'Zhu', 'Bachelors', 'Professional', 20220225080000),
(1, 40, 'Miller', 'Masters Degree', 'Management', 20220224080000),
(1, 50, 'Verhoff', 'Partial High School', 'Clerical', 20220225080000),
(1, 30, 'Zhu', 'Bachelors', 'Professional', 20220224090000),
(0, 50, 'Verhoff', 'Partial High School', 'Clerical', 20220226080000);

SELECT * FROM CDCStaging ORDER BY LoadTime




---------------------CREATE CDCProcessing TABLE------------------------
IF (OBJECT_ID('CDCProcessing') is not null) DROP TABLE CDCProcessing
CREATE TABLE CDCProcessing
	(SEQ int not null
	,ProductID int not null
	,Name nvarchar(255) not null
	,Category nvarchar(255) not null
	,Color nvarchar(255) not null
	,LoadTime bigint not null
	,ProcessingTime datetime default getdate()
	);
SELECT * FROM CDCProcessing


--------------------CREATE CDCHistory TABLE----------------------
IF (OBJECT_ID('CDCHistory') is not null) DROP TABLE CDCHistory
CREATE TABLE CDCHistory
	(SEQ int not null
	,ProductID int not null
	,Name nvarchar(255) not null
	,Category nvarchar(255) not null
	,Color nvarchar(255) not null
	,LoadTime bigint not null
	,ProcessingTime datetime default getdate());
SELECT * FROM CDCHistory


----------------CREATE CDCTarget TABLE----------------------------
IF (OBJECT_ID('CDCTarget') is not null) DROP TABLE CDCTarget
CREATE TABLE CDCTarget
	(ProductID int not null
	,Name nvarchar(255) not null
	,Category nvarchar(255) not null
	,Color nvarchar(255) not null
	);
SELECT * FROM CDCTarget



-------------THE SQL TRANSACTION COMMANDS-----------------

--MOVE DATA THAT HAS MIN DateInserted FROM CDCStaging TO CDCProcessing
BEGIN TRANSACTION;

INSERT INTO CDCProcessing(SEQ, ProductID, Name, Category, Color, LoadTime)
SELECT * FROM CDCStaging
WHERE LoadTime = (SELECT min(LoadTime) FROM CDCStaging);

DELETE FROM CDCStaging
WHERE LoadTime = (SELECT min(LoadTime) FROM CDCStaging);

COMMIT;

SELECT * FROM CDCStaging ORDER BY LoadTime
SELECT * FROM CDCProcessing ORDER BY ProductID

--MOVE UNWANTED DATA TO CDCHistory

--SELECT THE DATA GROUPBY ProductID WITH MAX SEQ "DATA TO BE MERGED"
--SELECT THE DATA NOT TO BE MERGED "MOVED TO HISTORY" BY SELECTING ALL DATA EXCEPT THE DATA TO BE MERGED
BEGIN TRANSACTION;

INSERT INTO CDCHistory (SEQ, ProductID, Name, Category, Color, LoadTime, ProcessingTime)
SELECT * FROM CDCProcessing
EXCEPT
SELECT Q.MAXSEQ AS SEQ, P.ProductID, P.Name, P.Category, P.Color, P.LoadTime, P.ProcessingTime 
FROM CDCProcessing AS P INNER JOIN (SELECT MAX (SEQ) AS MAXSEQ, ProductID AS QProductID FROM CDCProcessing GROUP BY ProductID) AS Q
ON Q.MAXSEQ = P.SEQ AND QProductID = P.ProductID


DELETE CDCProcessing
FROM CDCProcessing
INNER JOIN CDCHistory ON CDCProcessing.ProductID = CDCHistory.ProductID AND CDCProcessing.SEQ = CDCHistory.SEQ

COMMIT;

SELECT * FROM CDCProcessing
SELECT * FROM CDCHistory


--MERGE THE CDCProcessing WITH CDCTarget
MERGE CDCTarget AS Target
USING CDCProcessing	AS Source
ON Source.ProductID = Target.ProductID
    
-- For Inserts
WHEN NOT MATCHED BY Target THEN
    INSERT (ProductID, Name, Category, Color) 
    VALUES (Source.ProductID, Source.Name, Source.Category, Source.Color)
    
-- For Updates
WHEN MATCHED THEN
UPDATE
SET
    Target.ProductID = Source.ProductID,
	Target.Name	= Source.Name,
    Target.Category	= Source.Category,
    Target.Color	= Source.Color;

SELECT * FROM CDCProcessing
SELECT * FROM CDCTarget

--MOVE THE DATA IN CDCProcessing TO CDCHistory
BEGIN TRANSACTION;

INSERT INTO CDCHistory(SEQ, ProductID, Name, Category, Color, LoadTime, ProcessingTime)
SELECT * FROM CDCProcessing

DELETE FROM CDCProcessing

COMMIT;


--SELECT FROM TABLES

--Employee
SELECT * FROM CDCStagingEmployee ORDER BY LoadTime
SELECT * FROM CDCProcessingEmployee
SELECT * FROM CDCHistoryEmployee
SELECT * FROM CDCTargetEmployee

--Customer
SELECT * FROM CDCStagingCustomer ORDER BY LoadTime
SELECT * FROM CDCProcessingCustomer
SELECT * FROM CDCHistoryCustomer
SELECT * FROM CDCTargetCustomer

--Product
SELECT * FROM CDCStagingProduct ORDER BY LoadTime
SELECT * FROM CDCProcessingProduct
SELECT * FROM CDCHistoryProduct
SELECT * FROM CDCTargetProduct

--Date
SELECT * FROM CDCStagingDate ORDER BY LoadTime
SELECT * FROM CDCProcessingDate
SELECT * FROM CDCHistoryDate
SELECT * FROM CDCTargetDate

--Order
SELECT * FROM CDCStagingOrder ORDER BY LoadTime
SELECT * FROM CDCProcessingOrder
SELECT * FROM CDCHistoryOrder
SELECT * FROM CDCTargetOrder



--INSERT DUMMY DATA INTO CDCStagingProduct

INSERT INTO CDCStagingProduct (SEQ, ProductID, Name, Category, Color, LoadTime)
VALUES
(0, 50, 'Verhoff', 'Partial High School', 'Clerical', '2022-02-24 08:00:00.000'),
(0, 40, 'Miller', 'Masters Degree', 'Management', '2022-02-24 08:00:00.000'),
(2, 40, 'Miller', 'Masters Degree', 'Management', '2022-02-24 08:00:00.000'),
(0, 30, 'Zhu', 'Bachelors', 'Professional', '2022-02-24 08:00:00.000'),
(1, 30, 'Zhu', 'Bachelors', 'Professional', '2022-02-24 08:00:00.000'),
(0, 30, 'Zhu', 'Bachelors', 'Professional', '2022-02-24 09:00:00.000'),
(0, 40, 'Miller', 'Masters Degree', 'Management', '2022-02-25 08:00:00.000'),
(0, 50, 'Verhoff', 'Partial High School', 'Clerical', '2022-02-25 08:00:00.000'),
(0, 40, 'Miller', 'Masters Degree', 'Management', '2022-02-26 08:00:00.000'),
(0, 30, 'Zhu', 'Bachelors', 'Professional', '2022-02-26 08:00:00.000'),
(1, 40, 'Miller', 'Masters Degree', 'Management', '2022-02-25 08:00:00.000'),
(0, 50, 'Verhoff', 'Partial High School', 'Clerical', '2022-02-25 09:00:00.000'),
(0, 30, 'Zhu', 'Bachelors', 'Professional', '2022-02-25 08:00:00.000'),
(1, 40, 'Miller', 'Masters Degree', 'Management', '2022-02-24 08:00:00.000'),
(1, 50, 'Verhoff', 'Partial High School', 'Clerical', '2022-02-25 08:00:00.000'),
(1, 30, 'Zhu', 'Bachelors', 'Professional', '2022-02-24 09:00:00.000'),
(0, 50, 'Verhoff', 'Partial High School', 'Clerical', '2022-02-26 08:00:00.000');



SELECT * FROM CDCStagingProduct ORDER BY LoadTime







/* THE 2 SQL STATEMENTS
_________________________

SELECT * FROM CDCProcessing
EXCEPT
SELECT Q.MAXSEQ AS SEQ, P.ProductID, P.Name, P.Category, P.Color, P.LoadTime, P.ProcessingTime 
FROM CDCProcessing AS P INNER JOIN (SELECT MAX (SEQ) AS MAXSEQ, ProductID AS QProductID FROM CDCProcessing GROUP BY ProductID) AS Q
ON Q.MAXSEQ = P.SEQ AND QProductID = P.ProductID


select*
from product p1
where not exists (select 1
						from product p2
						where p2.pid = p1.pid
						and p2.seq > p1.seq
						group by seq)*/
