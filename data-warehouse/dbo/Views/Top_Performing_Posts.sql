CREATE VIEW [dbo].[Top_Performing_Posts]
AS
SELECT name,
       (post_like_count + comment_like_count + reactions + shares) AS total_engagement
FROM dim_facebook  d join
fact_facebook f
on d.page_id=f.page_id;