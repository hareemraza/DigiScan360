CREATE VIEW [dbo].[Comments_By_Weekday]
AS 
SELECT 
    DATENAME(WEEKDAY, created_date) AS weekday, 
    COUNT(comment_id) AS total_comments
FROM 
    fact_facebook
GROUP BY 
    DATENAME(WEEKDAY, created_date), 
    DATEPART(WEEKDAY, created_date);