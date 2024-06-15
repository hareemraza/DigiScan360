CREATE VIEW [dbo].[Total_Followers]
AS
SELECT page_id, SUM(followers_count) AS total_followers
FROM fact_facebook
GROUP BY page_id;