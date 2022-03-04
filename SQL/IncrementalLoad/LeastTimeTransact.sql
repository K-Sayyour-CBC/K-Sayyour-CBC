INSERT INTO CDCProcessing (SEQ, ProductID, ProductName, Category, Color, LoadTime)
SELECT * FROM CDCStaging
WHERE LoadTime = (SELECT min(LoadTime) FROM CDCStaging);
DELETE FROM CDCStaging
WHERE LoadTime = (SELECT min(LoadTime) FROM CDCStaging);