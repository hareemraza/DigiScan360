CREATE VIEW [dbo].[facebook_without_duplicates]
AS 
select DISTINCT comment_id as new_comment_id, page_id, post_id, fans_count, followers_count, shares, 
post_like_count, comment_like_count, reactions, created_date from fact_facebook
where page_id='page_6';