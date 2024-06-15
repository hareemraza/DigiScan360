-- Create a view for Engagement Rate

CREATE VIEW engagement_rate AS
SELECT 
    tweet_date,
    COUNT(tweet_id) AS total_tweets,
    SUM(like_count) AS total_likes,
    SUM(reply_count) AS total_replies,
    SUM(repost_count) AS total_reposts,
    SUM(quote_count) AS total_quotes,
    (SUM(like_count) + SUM(reply_count) + SUM(repost_count) + SUM(quote_count)) * 1.0 / COUNT(tweet_id) AS engagement_rate
FROM 
    fact_consumer_tweet
GROUP BY 
    tweet_date;