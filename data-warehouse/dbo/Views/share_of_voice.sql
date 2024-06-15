-- Create a view for Share of Voice

CREATE VIEW share_of_voice AS
SELECT 
    CASE 
        WHEN hashtags LIKE '%jbl%' THEN 'jbl'
        WHEN hashtags LIKE '%apple%' THEN 'apple'
        WHEN hashtags LIKE '%sony%' THEN 'sony'
        ELSE 'Other'
    END AS brand,
    COUNT(tweet_id) AS total_mentions
FROM 
    fact_consumer_tweet
GROUP BY 
    CASE 
        WHEN hashtags LIKE '%jbl%' THEN 'jbl'
        WHEN hashtags LIKE '%apple%' THEN 'apple'
        WHEN hashtags LIKE '%sony%' THEN 'sony'
        ELSE 'Other'
    END