-- Create a view to show total tweets and engagement rate for JBL brand
CREATE VIEW vw_sony_engagement_metrics AS
SELECT 
    dc.brand_name,
    COUNT(fct.tweet_id) AS total_tweets,
    SUM(fct.like_count + fct.reply_count + fct.repost_count) AS total_engagements,
    CASE 
        WHEN COUNT(fct.tweet_id) = 0 THEN 0
        ELSE CAST(SUM(fct.like_count + fct.reply_count + fct.repost_count) AS FLOAT) / COUNT(fct.tweet_id)
    END AS engagement_rate
FROM 
    dim_consumer dc
JOIN 
    fact_consumer_tweet fct ON dc.author_id = fct.author_id
WHERE 
    dc.brand_name = 'Sony'
GROUP BY 
    dc.brand_name;