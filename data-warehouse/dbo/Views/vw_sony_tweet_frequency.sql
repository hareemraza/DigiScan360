-- Create a view to show tweet frequency for JBL brand
CREATE VIEW vw_sony_tweet_frequency AS
SELECT 
    dc.brand_name,
    fct.tweet_date,
    COUNT(fct.tweet_id) AS tweet_count
FROM 
    dim_consumer dc
JOIN 
    fact_consumer_tweet fct ON dc.author_id = fct.author_id
WHERE 
    dc.brand_name = 'Sony'
GROUP BY 
    dc.brand_name, 
    fct.tweet_date