CREATE TABLE [dbo].[fact_consumer_tweet] (

	[tweet_id] varchar(255) NOT NULL, 
	[author_id] bigint NOT NULL, 
	[in_reply_to_user_id] bigint NOT NULL, 
	[timestamp] datetime2(6) NOT NULL, 
	[text] varchar(8000) NULL, 
	[impression_count] int NULL, 
	[like_count] int NULL, 
	[reply_count] int NULL, 
	[repost_count] int NULL, 
	[quote_count] int NULL, 
	[hashtags] varchar(8000) NULL, 
	[user_followers_count] int NULL, 
	[user_following_count] int NULL, 
	[verified] bit NULL, 
	[tweet_date] date NULL
);

