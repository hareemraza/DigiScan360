CREATE VIEW [dbo].[Average_Engagement_per_Page]
AS
SELECT page_id,
       (AVG(post_like_count) + AVG(comment_like_count) + AVG(reactions) + AVG(shares)) / 4 AS avg_engagement
FROM fact_facebook
GROUP BY page_id;