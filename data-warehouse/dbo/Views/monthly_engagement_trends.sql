--- View for Monthly Engagement Trends per Brand

CREATE VIEW monthly_engagement_trends AS
SELECT 
    dc.brand_name,
    YEAR(fct.tweet_date) AS year,
    MONTH(fct.tweet_date) AS month,
    SUM(fct.like_count + fct.reply_count + fct.quote_count) AS total_engagements
FROM 
    fact_consumer_tweet fct
JOIN 
    dim_consumer dc ON fct.author_id = dc.author_id
GROUP BY 
    dc.brand_name, YEAR(fct.tweet_date), MONTH(fct.tweet_date);