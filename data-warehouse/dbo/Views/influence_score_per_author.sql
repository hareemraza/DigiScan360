-- Influence Score per Author per Brand

CREATE VIEW influence_score_per_author AS
SELECT 
    dc.brand_name,
    fct.author_id,
    SUM(fct.like_count + fct.reply_count + fct.quote_count) AS total_engagements,
    MAX(fct.user_followers_count) AS followers_count,
    CASE 
        WHEN fct.verified = 1 THEN 1.5 
        ELSE 1 
    END AS verified_factor,
    (SUM(fct.like_count + fct.reply_count + fct.quote_count) * MAX(fct.user_followers_count) * CASE WHEN fct.verified = 1 THEN 1.5 ELSE 1 END) AS influence_score
FROM 
    fact_consumer_tweet fct
JOIN 
    dim_consumer dc ON fct.author_id = dc.author_id
GROUP BY 
    dc.brand_name, fct.author_id, fct.verified;