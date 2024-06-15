CREATE VIEW view_sony_engagement_rate AS
SELECT 
    tweet_date,
    COUNT(tweet_id) AS total_tweets,
    SUM(like_count) AS total_likes,
    SUM(reply_count) AS total_replies,
    SUM(repost_count) AS total_reposts,
    SUM(quote_count) AS total_quotes,
    SUM(impression_count) AS total_impressions,
    (SUM(like_count) + SUM(reply_count) + SUM(repost_count) + SUM(quote_count)) * 100.0 / SUM(impression_count) AS engagement_rate
FROM 
    fact_consumer_tweet
JOIN 
    dim_consumer ON fact_consumer_tweet.author_id = dim_consumer.author_id
WHERE 
    dim_consumer.brand_name = 'Sony'
GROUP BY 
    tweet_date