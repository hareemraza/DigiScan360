CREATE TABLE [dbo].[fact_products] (

	[ProductID] varchar(8000) NOT NULL, 
	[date_accessed] date NOT NULL, 
	[num_reviews] int NULL, 
	[rating] float NULL, 
	[rating_1] int NULL, 
	[rating_2] int NULL, 
	[rating_3] int NULL, 
	[rating_4] int NULL, 
	[rating_5] int NULL, 
	[price] float NULL
);


GO
ALTER TABLE [dbo].[fact_products] ADD CONSTRAINT pk_fact_products primary key NONCLUSTERED ([ProductID], [date_accessed]);