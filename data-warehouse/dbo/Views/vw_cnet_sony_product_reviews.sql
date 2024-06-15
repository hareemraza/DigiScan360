CREATE VIEW vw_cnet_sony_product_reviews AS
SELECT 
    product_name,
    NULLIF(REPLACE(REPLACE(strengths, '[', ''), ']', ''), '') AS strengths,
    NULLIF(REPLACE(REPLACE(weaknesses, '[', ''), ']', ''), '') AS weaknesses,
    rating,
    pros,
    cons,
    product_type
FROM 
    cnet_expert_review
WHERE 
    (REPLACE(REPLACE(strengths, '[', ''), ']', '') <> '' OR strengths IS NULL)
    AND (REPLACE(REPLACE(weaknesses, '[', ''), ']', '') <> '' OR weaknesses IS NULL)
    AND brand_name = 'Sony';