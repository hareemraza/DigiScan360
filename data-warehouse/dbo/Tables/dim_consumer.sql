CREATE TABLE [dbo].[dim_consumer] (

	[author_id] bigint NOT NULL, 
	[screen_name] varchar(255) NULL, 
	[lang] varchar(255) NULL, 
	[brand_name] varchar(255) NULL
);


GO
ALTER TABLE [dbo].[dim_consumer] ADD CONSTRAINT pk_dim_consumer_author_id primary key NONCLUSTERED ([author_id]);