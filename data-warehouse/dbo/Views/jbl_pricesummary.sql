CREATE VIEW [dbo].[jbl_pricesummary] AS (
SELECT 
    p.ProductID,
    p.title,
    round(fp.price, 2) as price,
    round(fp.rating, 2) as rating
FROM 
    dim_products AS p
JOIN 
    fact_products AS fp ON p.ProductID = fp.ProductID
WHERE 
    p.SellerID = 'sony' 
)