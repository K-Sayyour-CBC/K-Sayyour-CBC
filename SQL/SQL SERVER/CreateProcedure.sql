

--********************************************************************--
-- Create an ETL Stored Procedures
--********************************************************************--


--********************************************************************--
-- EXECUTE PROCEDURE
--********************************************************************--





--SELECT FROM TABLES

SELECT * FROM CDCStagingProduct ORDER BY LoadTime
SELECT * FROM CDCProcessingProduct
SELECT * FROM CDCHistoryProduct
SELECT * FROM CDCTargetProduct

TRUNCATE TABLE CDCHistoryProduct
TRUNCATE TABLE CDCTargetProduct

