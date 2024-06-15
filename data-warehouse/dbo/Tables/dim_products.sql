CREATE TABLE [dbo].[dim_products] (

	[ProductID] varchar(8000) NOT NULL, 
	[title] varchar(8000) NOT NULL, 
	[img_url] varchar(8000) NULL, 
	[product_url] varchar(8000) NULL, 
	[SellerID] varchar(8000) NULL
);


GO
ALTER TABLE [dbo].[dim_products] ADD CONSTRAINT pk_dim_products_ProductID primary key NONCLUSTERED ([ProductID]);