Create VIEW [dbo].[Engagement_Rate_Date]
AS SELECT created_time,
       (AVG(post_like_count) + AVG(comment_like_count) + AVG(reactions) + AVG(shares)) / 4 AS avg_engagement
FROM fact_facebook
GROUP BY created_time;