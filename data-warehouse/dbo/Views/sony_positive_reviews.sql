CREATE VIEW [dbo].[sony_positive_reviews] AS (SELECT 
    p.ProductID,
    p.title,
    fr.sentiment,
    fr.rating
FROM 
    dim_products AS p
JOIN 
    fact_products AS fp ON p.ProductID = fp.ProductID
JOIN
    fact_reviews AS fr ON fr.ProductID = p.ProductID
WHERE 
    p.SellerID = 'sony'  and sentiment = 1)