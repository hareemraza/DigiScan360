CREATE VIEW [dbo].[allbrands_sentiments] AS (SELECT 
    p.SellerID AS Brand,
    COUNT(CASE WHEN fr.sentiment = 1 THEN 1 ELSE NULL END) AS PositiveSentimentCount,
    COUNT(CASE WHEN fr.sentiment = 0 THEN 1 ELSE NULL END) AS NegativeSentimentCount
FROM 
    dim_products AS p
JOIN 
    fact_products AS fp ON p.ProductID = fp.ProductID
JOIN
    fact_reviews AS fr ON fr.ProductID = p.ProductID
-- WHERE 
--    p.SellerID IN ('sony', 'hyperx', 'samsung',  'xiaomi', 'beats')
GROUP BY 
    p.SellerID
)