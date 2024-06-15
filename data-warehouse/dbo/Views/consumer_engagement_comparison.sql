-- Create a view for Engagement Comparison by Verified Status

CREATE VIEW consumer_engagement_comparison AS
SELECT 
    CASE 
        WHEN verified = 1 THEN 'Verified'
        ELSE 'Non-Verified'
    END AS user_status,
    COUNT(tweet_id) AS total_tweets,
    SUM(like_count) AS total_likes,
    SUM(reply_count) AS total_replies,
    SUM(repost_count) AS total_reposts,
    SUM(quote_count) AS total_quotes,
    (SUM(like_count) + SUM(reply_count) + SUM(repost_count) + SUM(quote_count)) * 1.0 / COUNT(tweet_id) AS engagement_rate
FROM 
    fact_consumer_tweet
GROUP BY 
    CASE 
        WHEN verified = 1 THEN 'Verified'
        ELSE 'Non-Verified'
    END