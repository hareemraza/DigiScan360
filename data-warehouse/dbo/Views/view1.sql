CREATE VIEW [dbo].[view1]
AS 
SELECT 
created_date,
post_id,
count(distinct(post_id)) as post_count,
max(shares) as post_shares,
max(post_like_count) as post_like,
max(reactions) as post_reactions,
sum(comment_like_count) as sum_of_comment_likes,
count(new_comment_id) as total_comment_count
FROM facebook_without_duplicates
GROUP by created_date,
post_id;