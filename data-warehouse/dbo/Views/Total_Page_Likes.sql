CREATE VIEW [dbo].[Total_Page_Likes]
AS
SELECT page_id, SUM(fans_count) AS total_likes
FROM fact_facebook
GROUP BY page_id;