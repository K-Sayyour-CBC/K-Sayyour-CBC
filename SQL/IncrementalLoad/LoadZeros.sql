INSERT INTO CDCProcessed (SEQ, ProductID, ProductName, Category, Color)
SELECT SEQ, ProductID, ProductName, Category, Color FROM CDCProcessing
WHERE ProductID NOT IN (SELECT ProductID FROM CDCProcessing WHERE SEQ > 0);
DELETE FROM CDCProcessing
WHERE ProductID NOT IN (SELECT ProductID FROM CDCProcessing WHERE SEQ > 0);