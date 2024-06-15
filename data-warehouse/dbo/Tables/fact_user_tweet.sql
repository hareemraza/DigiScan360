CREATE TABLE [dbo].[fact_user_tweet] (

	[id] bigint NOT NULL, 
	[created_at] date NOT NULL, 
	[followers_count] int NULL, 
	[record_date] date NOT NULL, 
	[friends_count] int NULL, 
	[verified] bit NULL
);

