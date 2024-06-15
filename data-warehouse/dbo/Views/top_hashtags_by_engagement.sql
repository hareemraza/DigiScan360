-- Create a view for Top Hashtags by Engagement

CREATE VIEW top_hashtags_by_engagement AS
SELECT 
    hashtags,
    COUNT(tweet_id) AS total_tweets,
    SUM(impression_count) AS total_impressions,
    SUM(like_count) AS total_likes,
    SUM(reply_count) AS total_replies,
    SUM(repost_count) AS total_reposts,
    SUM(quote_count) AS total_quotes,
    (SUM(like_count) + SUM(reply_count) + SUM(repost_count) + SUM(quote_count)) * 1.0 / COUNT(tweet_id) AS engagement_rate
FROM 
    fact_consumer_tweet
GROUP BY 
    hashtags