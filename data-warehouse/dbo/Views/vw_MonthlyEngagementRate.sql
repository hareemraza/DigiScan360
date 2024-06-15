CREATE VIEW vw_MonthlyEngagementRate AS
WITH MonthlyEngagement AS (
    SELECT 
        c.brand_name,
        FORMAT(t.tweet_date, 'yyyy-MM') AS Month,
        SUM(t.like_count + t.reply_count + t.repost_count + t.quote_count) AS TotalEngagement,
        SUM(t.impression_count) AS TotalImpressions
    FROM 
        fact_consumer_tweet t
    JOIN 
        dim_consumer c
    ON 
        t.author_id = c.author_id
    GROUP BY 
        c.brand_name, 
        FORMAT(t.tweet_date, 'yyyy-MM')
)
SELECT 
    brand_name,
    Month,
    CASE 
        WHEN TotalImpressions = 0 THEN 0
        ELSE (TotalEngagement * 1.0 / TotalImpressions) * 100
    END AS EngagementRate
FROM 
    MonthlyEngagement