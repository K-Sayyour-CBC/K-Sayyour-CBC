BEGIN TRANSACTION;
INSERT INTO CDCHistory (SEQ, ProductID, Name, Category, Color, LoadTime, ProcessingTime)
SELECT * FROM CDCProcessing
EXCEPT
SELECT Q.MAXSEQ AS SEQ, P.ProductID, P.Name, P.Category, P.Color, P.LoadTime, P.ProcessingTime
FROM CDCProcessing AS P INNER JOIN (SELECT MAX(SEQ) AS MAXSEQ, ProductID AS QProductID FROM CDCProcessing GROUP BY ProductID) AS Q
ON Q.MAXSEQ = P.SEQ AND QProductID = P.ProductID
DELETE CDCProcessing
FROM CDCProcessing
INNER JOIN CDCHistory ON CDCProcessing.ProductID = CDCHistory.ProductID AND CDCProcessing.SEQ = CDCHistory.SEQ
COMMIT;