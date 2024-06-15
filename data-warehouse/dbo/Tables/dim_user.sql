CREATE TABLE [dbo].[dim_user] (

	[user_id] bigint NOT NULL, 
	[name] varchar(255) NULL, 
	[username] varchar(255) NULL, 
	[created_at] date NULL, 
	[url] varchar(255) NULL, 
	[followers_count] int NULL, 
	[record_date] date NULL
);


GO
ALTER TABLE [dbo].[dim_user] ADD CONSTRAINT pk_dim_user_user_id primary key NONCLUSTERED ([user_id]);