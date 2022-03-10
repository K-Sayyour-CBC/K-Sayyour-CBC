BEGIN TRANSACTION;
INSERT INTO CDCProcessing (SEQ, ProductID, Name, Category, Color, LoadTime)
SELECT * FROM CDCStaging
WHERE LoadTime = (SELECT min(LoadTime) FROM CDCStaging);
DELETE FROM CDCStaging
WHERE LoadTime = (SELECT min(LoadTime) FROM CDCStaging);
COMMIT;