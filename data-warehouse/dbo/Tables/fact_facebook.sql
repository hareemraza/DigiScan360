CREATE TABLE [dbo].[fact_facebook] (

	[page_id] varchar(255) NOT NULL, 
	[post_id] varchar(255) NOT NULL, 
	[created_time] datetime2(6) NOT NULL, 
	[fans_count] int NULL, 
	[followers_count] int NULL, 
	[message] varchar(8000) NULL, 
	[shares] int NULL, 
	[post_like_count] int NULL, 
	[comment_like_count] int NULL, 
	[reactions] int NULL, 
	[comment_id] varchar(255) NULL, 
	[from_user_id] varchar(255) NOT NULL, 
	[comment] varchar(8000) NULL, 
	[verified] bit NULL, 
	[created_date] date NULL
);

