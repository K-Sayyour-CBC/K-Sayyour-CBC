MERGE CDCTarget AS Target
USING CDCProcessing AS Source
ON Source.ProductID = Target.ProductID
WHEN NOT MATCHED BY Target THEN
  INSERT (ProductID, Name, Category, Color)
  VALUES (Source.ProductID, Source.Name, Source.Category, Source.Color)
WHEN MATCHED THEN
UPDATE
SET
  Target.ProductID = Source.ProductID,
  Target.Name = Source.Name,
  Target.Category = Source.Category,
  Target.Color = Source.Color;