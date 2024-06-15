CREATE VIEW [dbo].[allbrands_ratingandsentiments] AS (SELECT 
    sentiments.Brand,
    sentiments.PositiveSentimentCount,
    sentiments.NegativeSentimentCount,
    trends.Year,
    trends.Month,
    trends.rating,
    trends.RatingCount
FROM 
    (
        SELECT 
            p.SellerID AS Brand,
            COUNT(CASE WHEN fr.sentiment = 1 THEN 1 ELSE NULL END) AS PositiveSentimentCount,
            COUNT(CASE WHEN fr.sentiment = 0 THEN 1 ELSE NULL END) AS NegativeSentimentCount
        FROM 
            dim_products AS p
        JOIN 
            fact_products AS fp ON p.ProductID = fp.ProductID
        JOIN
            reviews AS fr ON fr.ProductID = p.ProductID
        GROUP BY 
            p.SellerID
    ) AS sentiments
JOIN 
    (
        SELECT 
            p.SellerID AS Brand,
            YEAR(r.date) AS Year,
            MONTH(r.date) AS Month,
            r.rating,
            COUNT(*) AS RatingCount
        FROM 
            reviews r
        JOIN 
            dim_products p ON r.ProductID = p.ProductID
        WHERE YEAR(r.date) >= 2020
        GROUP BY 
            p.SellerID, 
            YEAR(r.date), 
            MONTH(r.date), 
            r.rating
    ) AS trends
ON 
    sentiments.Brand = trends.Brand
)