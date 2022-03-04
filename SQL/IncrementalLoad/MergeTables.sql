MERGE CDCTarget AS Target
USING CDCProcessed AS Source
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