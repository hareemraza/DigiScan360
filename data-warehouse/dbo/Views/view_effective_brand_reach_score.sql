CREATE VIEW view_effective_brand_reach_score AS
SELECT 
    dc.brand_name,
    SUM(fct.like_count + fct.reply_count + fct.repost_count + fct.quote_count) AS Total_Engagements,
    SUM((fct.like_count + fct.reply_count + fct.repost_count + fct.quote_count) * fct.user_followers_count) AS Weighted_Engagements,
    (SUM((fct.like_count + fct.reply_count + fct.repost_count + fct.quote_count) * fct.user_followers_count) / NULLIF(SUM(fct.user_followers_count), 0)) * 1000 AS Effective_Brand_Reach_Score
FROM 
    fact_consumer_tweet fct
JOIN 
    dim_consumer dc ON fct.author_id = dc.author_id
GROUP BY 
    dc.brand_name