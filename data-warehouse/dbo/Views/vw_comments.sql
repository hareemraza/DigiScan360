CREATE VIEW [dbo].[vw_comments]
AS 
SELECT
    f.created_date,
    d.name,
    COUNT(*) AS comment_count
FROM
    fact_facebook f
JOIN
    dim_facebook d ON f.page_id = d.page_id
WHERE
    d.name = 'audio-technica'
GROUP BY
    f.created_date, d.name;