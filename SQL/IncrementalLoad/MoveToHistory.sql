BEGIN TRANSACTION;
INSERT INTO CDCHistory (SEQ, ProductID, Name, Category, Color, LoadTime, ProcessingTime)
SELECT * FROM CDCProcessing
DELETE FROM CDCProcessing
COMMIT;