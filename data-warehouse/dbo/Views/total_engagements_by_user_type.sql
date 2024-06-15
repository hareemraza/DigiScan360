--- View for Total Engagements by Verified and Non-Verified Users per Brand

CREATE VIEW total_engagements_by_user_type AS
SELECT 
    dc.brand_name,
    CASE WHEN fct.verified = 1 THEN 'Verified' ELSE 'Non-Verified' END AS user_type,
    COUNT(fct.tweet_id) AS total_tweets,
    SUM(fct.like_count + fct.reply_count + fct.quote_count) AS total_engagements
FROM 
    fact_consumer_tweet fct
JOIN 
    dim_consumer dc ON fct.author_id = dc.author_id
GROUP BY 
    dc.brand_name, fct.verified;