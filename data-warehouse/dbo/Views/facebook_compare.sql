CREATE VIEW [dbo].[facebook_compare]
AS SELECT distinct ff.comment_id as new_comment_id, df.page_id, df.name, ff.post_id, ff.fans_count, 
ff.followers_count, ff.shares, ff.post_like_count, ff.comment_like_count, ff.reactions, 
ff.verified, ff.created_date
FROM fact_facebook ff
join dim_facebook df on ff.page_id=df.page_id