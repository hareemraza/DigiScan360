CREATE VIEW [dbo].[Fan_Growth_Rate]
AS 
SELECT 
    page_id, 
    (MAX(fans_count) - MIN(fans_count)) / COUNT(DISTINCT created_date) AS daily_fan_growth_rate
FROM 
    fact_facebook
GROUP BY 
    page_id;