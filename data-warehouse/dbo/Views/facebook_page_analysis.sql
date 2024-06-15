CREATE VIEW [dbo].[facebook_page_analysis]
AS 
SELECT
    COUNT(DISTINCT ff.post_id) AS total_posts,
    SUM(ff.fans_count) AS total_fans_count,
    SUM(ff.followers_count) AS total_followers_count,
    SUM(ff.shares) AS total_shares,
    SUM(ff.post_like_count) AS total_post_like_count,
    SUM(ff.comment_like_count) AS total_comment_like_count,
    SUM(ff.reactions) AS total_reactions,
    AVG((ff.shares + ff.post_like_count + ff.comment_like_count + ff.reactions) / NULLIF(ff.fans_count + ff.followers_count, 0)) * 100 AS avg_engagement_rate
FROM
    fact_facebook ff
INNER JOIN
    dim_facebook df ON ff.page_id = df.page_id
WHERE
    df.name = 'audio-technica'
GROUP BY
    MONTH(ff.created_date), YEAR(ff.created_date)