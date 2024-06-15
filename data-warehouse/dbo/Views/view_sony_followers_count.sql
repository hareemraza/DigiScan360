CREATE VIEW view_sony_followers_count AS
SELECT 
    du.name AS brand_name,
    MAX(fut.followers_count) AS total_followers_count
FROM 
    dim_user du
JOIN 
    fact_user_tweet fut ON du.user_id = fut.id
WHERE 
    du.name = 'Sony'
    AND fut.record_date = (
        SELECT MAX(fut_inner.record_date)
        FROM fact_user_tweet fut_inner
        WHERE fut_inner.id = du.user_id
    )
GROUP BY 
    du.name;