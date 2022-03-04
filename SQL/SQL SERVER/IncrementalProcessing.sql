

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
	,ProductName nvarchar(255) not null
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

--MOVE UNWANTED DATA TO CDCHistory

--SELECT THE DATA GROUPBY ProductID WITH MAX SEQ "DATA TO BE MERGED"
--SELECT THE DATA NOT TO BE MERGED "MOVED TO HISTORY" BY SELECTING ALL DATA EXCEPT THE DATA TO BE MERGED
BEGIN TRANSACTION;

INSERT INTO CDCHistory(SEQ, ProductID, ProductName, Category, Color, LoadTime, ProcessingTime)
SELECT * FROM CDCProcessing
EXCEPT
SELECT Q.MAXSEQ AS SEQ, P.ProductID, P.ProductName, P.Category, P.Color, P.LoadTime, P.ProcessingTime 
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

SELECT * FROM CDCProcessing
SELECT * FROM CDCTarget

--MOVE THE DATA IN CDCProcessing TO CDCHistory
BEGIN TRANSACTION;

INSERT INTO CDCHistory(SEQ, ProductID, ProductName, Category, Color, LoadTime, ProcessingTime)
SELECT * FROM CDCProcessing

DELETE FROM CDCProcessing

COMMIT;

SELECT * FROM CDCStaging ORDER BY LoadTime
SELECT * FROM CDCProcessing
SELECT * FROM CDCHistory
SELECT * FROM CDCTarget


--ToHistoryFile
INSERT INTO CDCHistory (SEQ, ProductID, ProductName, Category, Color, LoadTime, ProcessingTime)
SELECT * FROM CDCProcessing
EXCEPT
SELECT Q.MAXSEQ AS SEQ, P.ProductID, P.ProductName, P.Category, P.Color, P.LoadTime, P.ProcessingTime
FROM CDCProcessing AS P INNER JOIN (SELECT MAX(SEQ) AS MAXSEQ, ProductID AS QProductID FROM CDCProcessing GROUP BY ProductID) AS Q
ON Q.MAXSEQ = P.SEQ AND QProductID = P.ProductID
DELETE CDCProcessing
FROM CDCProcessing
INNER JOIN CDCHistory ON CDCProcessing.ProductID = CDCHistory.ProductID AND CDCProcessing.SEQ = CDCHistory.SEQ

--MergeTablesFile
MERGE CDCTarget AS Target
USING CDCProcessing AS Source
ON Source.ProductID = Target.ProductID
WHEN NOT MATCHED BY Target THEN
  INSERT (ProductID, ProductName, Category, Color)
  VALUES (Source.ProductID, Source.ProductName, Source.Category, Source.Color)
WHEN MATCHED THEN
UPDATE
SET
  Target.ProductID = Source.ProductID,
  Target.ProductName = Source.ProductName,
  Target.Category = Source.Category,
  Target.Color = Source.Color;

--MoveToHistory
INSERT INTO CDCHistory (SEQ, ProductID, ProductName, Category, Color, LoadTime, ProcessingTime)
SELECT * FROM CDCProcessing
DELETE FROM CDCProcessing

