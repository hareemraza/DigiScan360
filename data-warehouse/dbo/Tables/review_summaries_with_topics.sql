CREATE TABLE [dbo].[review_summaries_with_topics] (

	[review_fk] int NOT NULL, 
	[ProductID] varchar(8000) NOT NULL, 
	[sentiment] bit NULL, 
	[summary] varchar(8000) NULL, 
	[topic] varchar(8000) NULL, 
	[SellerID] varchar(8000) NULL
);

