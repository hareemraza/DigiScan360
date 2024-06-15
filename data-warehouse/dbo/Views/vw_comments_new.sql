CREATE VIEW [dbo].[vw_comments_new]
AS
SELECT
    f.created_date,
    d.name,
    COUNT(*) AS comment_count
FROM
    fact_facebook f
JOIN
    dim_facebook d ON f.page_id = d.page_id
JOIN
    dim_time t ON f.created_date = t.date
WHERE
    d.name = 'audio-technica'
    AND t.date =f.created_date -- Assuming the month column in dim_time is named 'month'
GROUP BY
    f.created_date, d.name;