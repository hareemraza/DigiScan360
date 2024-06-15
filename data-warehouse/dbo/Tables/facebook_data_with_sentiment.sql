CREATE TABLE [dbo].[facebook_data_with_sentiment] (

	[id] varchar(8000) NULL, 
	[contact_address] varchar(8000) NULL, 
	[current_location] varchar(8000) NULL, 
	[emails] varchar(8000) NULL, 
	[fan_count] int NULL, 
	[followers_count] int NULL, 
	[name] varchar(8000) NULL, 
	[username] varchar(8000) NULL, 
	[post_id] varchar(8000) NULL, 
	[created_time9] datetime2(6) NULL, 
	[message] varchar(8000) NULL, 
	[shares] int NULL, 
	[likes] int NULL, 
	[reactions] int NULL, 
	[comment_id] varchar(8000) NULL, 
	[created_time15] datetime2(6) NULL, 
	[from] varchar(8000) NULL, 
	[like_count] int NULL, 
	[comment] varchar(8000) NULL, 
	[verified] bit NULL, 
	[sentiment] bit NULL
);

