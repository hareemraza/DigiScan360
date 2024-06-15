CREATE VIEW [dbo].[allbrands_ratingtrends] AS (SELECT 
    p.SellerID AS Brand,
    YEAR(r.date) AS Year,
    MONTH(r.date) AS Month,
    r.rating,
    COUNT(*) AS RatingCount
FROM 
    fact_reviews r
JOIN 
    dim_products p ON r.ProductID = p.ProductID
WHERE YEAR(r.date) >= 2020
GROUP BY 
    p.SellerID, 
    YEAR(r.date), 
    MONTH(r.date), 
    r.rating

)