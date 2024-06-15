CREATE VIEW monthly_engagement_rate AS
SELECT 
    dt.year,
    COUNT(fct.tweet_id) AS TotalTweets,
    SUM(fct.like_count) AS TotalLikes,
    SUM(fct.repost_count) AS TotalReposts,
    SUM(fct.reply_count) AS TotalReplies,
    SUM(fct.user_followers_count) AS TotalFollowers,
    SUM(fct.like_count + fct.repost_count + fct.reply_count) AS TotalEngagements,
    CASE 
        WHEN SUM(fct.user_followers_count) = 0 THEN 0
        ELSE SUM(fct.like_count + fct.repost_count + fct.reply_count) / CAST(SUM(fct.user_followers_count) AS FLOAT)
    END AS EngagementRate
FROM 
    fact_consumer_tweet fct
JOIN 
    dim_time dt ON CAST(fct.timestamp AS DATE) = dt.date
GROUP BY 
    dt.year;