CREATE VIEW followers_growth AS
WITH FollowerGrowth AS (
    SELECT
        fut.id,
        du.name AS company_name,
        dt.year,
        dt.month,
        fut.record_date,
        fut.followers_count,
        LAG(fut.followers_count) OVER (PARTITION BY fut.id ORDER BY fut.record_date) AS previous_followers_count
    FROM
        fact_user_tweet fut
    JOIN
        dim_user du ON fut.id = du.user_id
    JOIN
        dim_time dt ON CAST(fut.record_date AS DATE) = dt.date
)
SELECT
    company_name,
    year,
    month,
    record_date,
    followers_count,
    previous_followers_count,
    CASE 
        WHEN previous_followers_count IS NULL THEN NULL
        ELSE (followers_count - previous_followers_count) * 100.0 / previous_followers_count
    END AS growth_rate
FROM
    FollowerGrowth;