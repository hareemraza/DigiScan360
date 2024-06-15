CREATE TABLE [dbo].[reviews] (

	[ProductID] varchar(8000) NOT NULL, 
	[date] date NULL, 
	[rating] int NULL, 
	[num_helpful] int NULL, 
	[sentiment] bit NULL, 
	[id] int NOT NULL, 
	[review_id] varchar(8000) NULL
);


GO
ALTER TABLE [dbo].[reviews] ADD CONSTRAINT pk_fact_reviews_id primary key NONCLUSTERED ([id]);