CREATE TABLE CDCTargetOrder
(OrderID int  primary key
,ProductID int  not null
,CustomerID int  not null
,DateKey int  not null
,Price float  not null
,Quantity int  not null

);