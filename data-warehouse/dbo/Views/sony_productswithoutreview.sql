CREATE VIEW [dbo].[sony_productswithoutreview] AS (SELECT p.ProductID, p.title, p.img_url, p.SellerID, fp.date_accessed, fp.num_reviews, ROUND(fp.rating, 2) as rating, fp.rating_1, fp.rating_2, fp.rating_3, fp.rating_4, fp.rating_5, ROUND(fp.price,2) as price
FROM 
    dim_products AS p
JOIN 
    fact_products AS fp ON p.ProductID = fp.ProductID
WHERE 
    p.SellerID = 'sony' 
)