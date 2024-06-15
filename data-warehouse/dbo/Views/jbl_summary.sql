CREATE VIEW [dbo].[jbl_summary] AS (SELECT 
    p.ProductID,
    p.title,
    SUM(fp.num_reviews) AS Total_Reviews,
    ROUND(AVG(fp.rating), 2) AS Average_Rating,  -- Rounding the average rating to 2 decimal places
    SUM(fp.rating_1) AS Rating_1,
    SUM(fp.rating_2) AS Rating_2,
    SUM(fp.rating_3) AS Rating_3,
    SUM(fp.rating_4) AS Rating_4,
    SUM(fp.rating_5) AS Rating_5
FROM 
    dim_products AS p
JOIN 
    fact_products AS fp ON p.ProductID = fp.ProductID
WHERE 
    p.SellerID = 'sony'  
GROUP BY 
    p.ProductID, p.title
)