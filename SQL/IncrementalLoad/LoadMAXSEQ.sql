INSERT INTO CDCProcessed (SEQ, ProductID, ProductName, Category, Color)
SELECT SEQ, ProductID, ProductName, Category, Color FROM CDCProcessing
WHERE SEQ = (SELECT MAX(SEQ) FROM CDCProcessing GROUP BY ProductID);
DELETE FROM CDCProcessing
WHERE SEQ = (SELECT MAX(SEQ) FROM CDCProcessing GROUP BY ProductID);