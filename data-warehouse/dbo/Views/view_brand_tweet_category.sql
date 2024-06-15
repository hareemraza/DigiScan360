CREATE VIEW view_brand_tweet_category AS
SELECT 
    dc.brand_name,
    CASE
        WHEN fct.hashtags LIKE '%headphones%' OR fct.text LIKE '%headphone%' THEN 'Headphones'
        WHEN fct.hashtags LIKE '%earbuds%' OR fct.text LIKE '%earbud%' THEN 'Earbuds'
        WHEN fct.hashtags LIKE '%speaker%' OR fct.text LIKE '%speaker%' THEN 'Speakers'
        WHEN fct.hashtags LIKE '%gaming%' OR fct.text LIKE '%gaming%' THEN 'Gaming'
        WHEN fct.hashtags LIKE '%travel%' OR fct.text LIKE '%travel%' THEN 'Travel'
        WHEN fct.hashtags LIKE '%fitness%' OR fct.text LIKE '%fitness%' 
             OR fct.hashtags LIKE '%workout%' OR fct.text LIKE '%workout%' THEN 'Fitness'
        WHEN fct.hashtags LIKE '%noise%' AND (fct.text LIKE '%cancelling%' OR fct.text LIKE '%canceling%') THEN 'Noise Cancelling'
        ELSE 'Other'
    END AS product_category,
    COUNT(fct.tweet_id) AS total_tweets
FROM 
    dim_consumer dc
JOIN 
    fact_consumer_tweet fct ON dc.author_id = fct.author_id
GROUP BY 
    dc.brand_name,
    CASE
        WHEN fct.hashtags LIKE '%headphones%' OR fct.text LIKE '%headphone%' THEN 'Headphones'
        WHEN fct.hashtags LIKE '%earbuds%' OR fct.text LIKE '%earbud%' THEN 'Earbuds'
        WHEN fct.hashtags LIKE '%speaker%' OR fct.text LIKE '%speaker%' THEN 'Speakers'
        WHEN fct.hashtags LIKE '%gaming%' OR fct.text LIKE '%gaming%' THEN 'Gaming'
        WHEN fct.hashtags LIKE '%travel%' OR fct.text LIKE '%travel%' THEN 'Travel'
        WHEN fct.hashtags LIKE '%fitness%' OR fct.text LIKE '%fitness%' 
             OR fct.hashtags LIKE '%workout%' OR fct.text LIKE '%workout%' THEN 'Fitness'
        WHEN fct.hashtags LIKE '%noise%' AND (fct.text LIKE '%cancelling%' OR fct.text LIKE '%canceling%') THEN 'Noise Cancelling'
        ELSE 'Other'
    END;