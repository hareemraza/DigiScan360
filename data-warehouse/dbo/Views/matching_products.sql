CREATE VIEW [dbo].[matching_products] AS (SELECT DISTINCT 
    rp.ProductID,
    rp.Title,
    rp.Rating,
    rp.sharedFeatures,
    rp.MatchingProductID,
    rp.MatchingProductTitle,
    rp.MatchingSeller,
    rp.MatchingProductRating,
    rp.img_url,
    rp.num_reviews
FROM (
    SELECT 
        smp.ProductID,
        smp.Title,
        smp.Rating,
        smp.sharedFeatures,
        smp.MatchingProductID,
        smp.MatchingProductTitle,
        smp.MatchingSeller,
        smp.MatchingProductRating,
        p.img_url,
        T.num_reviews,
        ROW_NUMBER() OVER (PARTITION BY smp.ProductID ORDER BY smp.ProductID) AS row_num
    FROM sony_matching_products smp
    JOIN dim_products p ON smp.MatchingProductID = p.ProductID
    JOIN reviews r ON p.ProductID = r.ProductID
    JOIN (
        SELECT ProductID, COUNT(*) AS num_reviews
        FROM reviews
        GROUP BY ProductID
    ) AS T ON T.ProductID = p.ProductID
    WHERE smp.MatchingSeller IN ('xiaomi', 'panasonic', 'lenovo', 'logitech g', 'soundcore', 'jbl', 'apple', 'logitech', 'philips', 'skullcandy', 'iclever', 'razer', 'sennheiser')
) AS rp
WHERE rp.row_num <= 10
)