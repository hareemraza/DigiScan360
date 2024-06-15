CREATE VIEW [dbo].[check_yearlyratings] AS (SELECT TOP 10
    p.SellerID AS Brand,
    t.year,
    AVG(fp.rating) AS avg_rating,
    COUNT(fp.rating) AS rating_count  -- Adding count of ratings
FROM 
    fact_products fp
JOIN 
    dim_products p ON fp.ProductID = p.ProductID
JOIN 
    dim_time t ON fp.date_accessed = t.date
GROUP BY 
    p.SellerID, t.year
ORDER BY 
    t.year, rating_count DESC, p.SellerID -- Ordering by year and count of ratings, then SellerID
)