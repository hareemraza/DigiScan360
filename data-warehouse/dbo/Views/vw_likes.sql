CREATE VIEW [dbo].[vw_likes]
AS 
SELECT
    f.created_date,
    d.name,
    SUM(f.post_like_count + f.comment_like_count + f.reactions) AS like_count
FROM
    fact_facebook f
JOIN
    dim_facebook d ON f.page_id = d.page_id
WHERE
    d.name = 'audio-technica'
GROUP BY
    f.created_date, d.name;