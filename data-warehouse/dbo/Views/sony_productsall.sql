CREATE VIEW [dbo].[sony_productsall] AS (SELECT p.ProductID, p.title, p.img_url, p.SellerID, fp.date_accessed, fp.num_reviews, ROUND(fp.rating, 2) as rating, fp.rating_1, fp.rating_2, fp.rating_3, fp.rating_4, fp.rating_5, ROUND(fp.price,2) as price, fr.rating as review_rating, fr.num_helpful, fr.sentiment 
FROM 
    dim_products AS p
JOIN 
    fact_products AS fp ON p.ProductID = fp.ProductID
JOIN 
    fact_reviews AS fr ON p.ProductID = fr.ProductID
WHERE 
    p.SellerID = 'sony' 
)