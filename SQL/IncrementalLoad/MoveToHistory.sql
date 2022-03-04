INSERT INTO CDCHistory (SEQ, ProductID, ProductName, Category, Color, LoadTime, ProcessingTime)
SELECT * FROM CDCProcessing
DELETE FROM CDCProcessing