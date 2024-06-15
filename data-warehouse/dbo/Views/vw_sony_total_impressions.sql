-- Create a view to show total impressions for JBL brand
CREATE VIEW vw_sony_total_impressions AS
SELECT 
    dc.brand_name,
    SUM(fct.impression_count) AS total_impressions
FROM 
    dim_consumer dc
JOIN 
    fact_consumer_tweet fct ON dc.author_id = fct.author_id
WHERE 
    dc.brand_name = 'Sony'
GROUP BY 
    dc.brand_name;