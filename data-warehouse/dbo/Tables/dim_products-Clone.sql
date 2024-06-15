CREATE TABLE [dbo].[dim_products-Clone] (

	[ProductID] varchar(8000) NOT NULL, 
	[title] varchar(8000) NOT NULL, 
	[img_url] varchar(8000) NULL, 
	[product_url] varchar(8000) NULL, 
	[SellerID] varchar(8000) NULL
);


GO
ALTER TABLE [dbo].[dim_products-Clone] ADD CONSTRAINT PK__dim_prod__B40CC6ECA551673A primary key NONCLUSTERED ([ProductID]);