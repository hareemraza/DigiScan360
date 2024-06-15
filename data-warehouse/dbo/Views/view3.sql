CREATE VIEW [dbo].[view3]
AS 
WITH MonthlyEngagement AS (
    SELECT 
        c.brand_name,
        DATEFROMPARTS(YEAR(t.tweet_date), MONTH(t.tweet_date), 1) AS Month,
        SUM(t.like_count + t.reply_count + t.repost_count + t.quote_count) AS TotalEngagement,
        SUM(t.impression_count) AS TotalImpressions,
        t.author_id  -- Adding more granularity to make each row unique
    FROM 
        fact_consumer_tweet t
    JOIN 
        dim_consumer c
    ON 
        t.author_id = c.author_id
    GROUP BY 
        c.brand_name, 
        DATEFROMPARTS(YEAR(t.tweet_date), MONTH(t.tweet_date), 1),
        t.author_id
)
SELECT 
    brand_name,
    Month,
    CASE 
        WHEN TotalImpressions = 0 THEN 0
        ELSE (TotalEngagement * 1.0 / TotalImpressions) * 100
    END AS EngagementRate,
    author_id  -- Including author_id in the final view
FROM 
    MonthlyEngagement;