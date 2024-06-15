CREATE VIEW vw_brand_engagement_over_time AS
SELECT 
    dc.brand_name,
    CAST(DATEADD(MONTH, DATEDIFF(MONTH, 0, fct.tweet_date), 0) AS DATE) AS month,
    SUM(fct.like_count + fct.reply_count + fct.repost_count + fct.quote_count) AS Total_Engagements,
    COUNT(DISTINCT fct.tweet_id) AS Total_Tweets,
    (SUM(fct.like_count + fct.reply_count + fct.repost_count + fct.quote_count) / NULLIF(COUNT(DISTINCT fct.tweet_id), 0)) AS Engagement_Rate
FROM 
    fact_consumer_tweet fct
JOIN 
    dim_consumer dc ON fct.author_id = dc.author_id
GROUP BY 
    dc.brand_name, DATEADD(MONTH, DATEDIFF(MONTH, 0, fct.tweet_date), 0);