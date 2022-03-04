

/*select * from CDCStaging order by DateInserted ASC
-- create CDCProcessing same schema + ProcessingTime 
-- move all rows with the oldest DateInserted timestamp

-- 0	50	Yang	Bachelors	Professional	20220224080000
-- 0	40	Johnson	Masters Degree	Management	20220224080000
-- 0	30	Torres	Partial College	Skilled Manual	20220224080000
-- 1	40	Verhoff	Partial High School	Clerical	20220224080000

-- Transaction Begin 
-- Select * into CDCProcessing from CDCStaging where DateInserted = '20220224080000'
-- Delete from CDCStaging where DateInserted = '20220224080000'
-- UPDATE [dbo].[CDCProcessing] SET ProcessingTime = getdate() WHERE ProcessingTime is null 
-- select [ProductID], Count(SEQ) as CountSEQ from [dbo].[CDCProcessing] Group by ProductID Having CountSEQ > 1
-- select [ProductID], Count(SEQ) from [dbo].[CDCProcessing] Group by ProductID 
-- moving the unwanted seq. into history 
-- history needs a ProcessingTime column too 

-- 
-- Select SEQ from CDCProcessing where ProductID = '40' and SEQ < (Select MAX(SEQ) from CDCProcessing where ProductID = '40')
-- move from Processing to History 


Select * from [dbo].[CDCProcessing] where ProductID = '40' and SEQ <



-- Transaction End */

-----------------CREATE CDCStaging TABLE--------------

IF (OBJECT_ID('CDCStaging') is not null) DROP TABLE CDCStaging
CREATE TABLE CDCStaging
	(SEQ int not null
	,ProductID int not null
	,ProductName nvarchar(255) not null
	,Category nvarchar(255) not null
	,Color nvarchar(255) not null
	,LoadTime bigint not null
	);
INSERT INTO CDCStaging
VALUES
(0, 50, 'Verhoff', 'Partial High School', 'Clerical', 20220224080000),
(0, 40, 'Miller', 'Masters Degree', 'Management', 20220224080000),
(0, 30, 'Zhu', 'Bachelors', 'Professional', 20220224080000),
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
	,ProductName nvarchar(255) not null
	,Category nvarchar(255) not null
	,Color nvarchar(255) not null
	,LoadTime bigint not null
	,ProcessingTime datetime default getdate()
	);
SELECT * FROM CDCProcessing

---------------------CREATE CDCProcessed TABLE-------------------------
IF (OBJECT_ID('CDCProcessed') is not null) DROP TABLE CDCProcessed
CREATE TABLE CDCProcessed  
(SEQ int not null
,ProductID int not null
,ProductName nvarchar(255) not null
,Category nvarchar(255) not null
,Color nvarchar(255) not null);
SELECT * FROM CDCProcessed

--------------------CREATE CDCHistory TABLE----------------------
IF (OBJECT_ID('CDCHistory') is not null) DROP TABLE CDCHistory
CREATE TABLE CDCHistory
	(SEQ int not null
	,ProductID int not null
	,ProductName nvarchar(255) not null
	,Category nvarchar(255) not null
	,Color nvarchar(255) not null
	,LoadTime bigint not null
	,ProcessingTime datetime default getdate());
SELECT * FROM CDCHistory



----------------CREATE CDCTarget TABLE----------------------------
IF (OBJECT_ID('CDCTarget') is not null) DROP TABLE CDCTarget
CREATE TABLE CDCTarget
	(ProductID int not null
	,ProductName nvarchar(255) not null
	,Category nvarchar(255) not null
	,Color nvarchar(255) not null
	);
SELECT * FROM CDCTarget

-------------THE SQL TRANSACTION COMMANDS-----------------

--MOVE DATA THAT HAS MIN DateInserted FROM CDCStaging TO CDCProcessing
BEGIN TRANSACTION;

INSERT INTO CDCProcessing (SEQ, ProductID, ProductName, Category, Color, LoadTime)
SELECT * FROM CDCStaging
WHERE LoadTime = (SELECT min(LoadTime) FROM CDCStaging);

DELETE FROM CDCStaging
WHERE LoadTime = (SELECT min(LoadTime) FROM CDCStaging);

COMMIT;

SELECT * FROM CDCStaging ORDER BY LoadTime
SELECT * FROM CDCProcessing ORDER BY ProductID

--SEND THE DATA THAT HAS ONLY 0 SEQ TO CDCProcessed 
BEGIN TRANSACTION;

INSERT INTO CDCProcessed (SEQ, ProductID, ProductName, Category, Color)
SELECT SEQ, ProductID, ProductName, Category, Color FROM CDCProcessing
WHERE ProductID NOT IN (SELECT ProductID FROM CDCProcessing WHERE SEQ > 0);

DELETE FROM CDCProcessing
WHERE ProductID NOT IN (SELECT ProductID FROM CDCProcessing WHERE SEQ > 0);

COMMIT;

SELECT * FROM CDCProcessing
SELECT * FROM CDCProcessed

--MOVE FROM THE REMAINING DATA, THE DATA WITH ProductID HAVING MAX SEQ
BEGIN TRANSACTION;

INSERT INTO CDCProcessed (SEQ, ProductID, ProductName, Category, Color)
SELECT SEQ, ProductID , ProductName, Category, Color FROM CDCProcessing
WHERE SEQ = (SELECT MAX(SEQ) FROM CDCProcessing GROUP BY ProductID);

DELETE FROM CDCProcessing
WHERE SEQ = (SELECT MAX(SEQ) FROM CDCProcessing GROUP BY ProductID);

COMMIT;

SELECT * FROM CDCProcessing
SELECT * FROM CDCProcessed

--MOVE THE RAMAINING DATA TO HISTORY
BEGIN TRANSACTION;

INSERT INTO CDCHistory (SEQ, ProductID, ProductName, Category, Color, LoadTime, ProcessingTime)
SELECT * FROM CDCProcessing

DELETE FROM CDCProcessing
SELECT * FROM CDCProcessing;

COMMIT;

--SELECT DATA FROM TABLES
SELECT * FROM CDCStaging ORDER BY LoadTime
SELECT * FROM CDCProcessing
SELECT * FROM CDCProcessed
SELECT * FROM CDCHistory
SELECT * FROM CDCTarget


--MERGE THE CDCProcessed WITH CDCTarget
MERGE CDCTarget AS Target
USING CDCProcessed	AS Source
ON Source.ProductID = Target.ProductID
    
-- For Inserts
WHEN NOT MATCHED BY Target THEN
    INSERT (ProductID, ProductName, Category, Color) 
    VALUES (Source.ProductID, Source.ProductName, Source.Category, Source.Color)
    
-- For Updates
WHEN MATCHED THEN
UPDATE
SET
    Target.ProductID = Source.ProductID,
	Target.ProductName	= Source.ProductName,
    Target.Category	= Source.Category,
    Target.Color	= Source.Color;

TRUNCATE TABLE CDCProcessed

SELECT * FROM CDCProcessed
SELECT * FROM CDCTarget




--ProductID  (SELECT ProductID, MAX(SEQ) AS MAXSEQ , COUNT(*)AS Occurence FROM CDCProcessing GROUP BY (ProductID) HAVING (COUNT(*) > 1))
--SQL Cursor
/*DECLARE @ProductID int;
DECLARE Crs CURSOR 
	FOR SELECT ProductID FROM CDCProcessing;
OPEN Crs;
FETCH NEXT FROM Crs INTO @ProductID;
WHILE @@FETCH_STATUS = 0
	BEGIN
		PRINT @ProductID
	END;
CLOSE Crs;
DEALLOCATE Crs;*/