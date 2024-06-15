-- Create a view to show top hashtags used by JBL brand 
CREATE VIEW vw_sony_top_hashtags AS
SELECT 
    dc.brand_name,
    ht.cleaned_hashtag AS hashtag,
    COUNT(*) AS hashtag_count
FROM 
    dim_consumer dc
JOIN 
    fact_consumer_tweet fct ON dc.author_id = fct.author_id
CROSS APPLY (
    SELECT 
        LTRIM(RTRIM(REPLACE(REPLACE(REPLACE(REPLACE(value, '[', ''), ']', ''), '#', ''), ',', ''))) AS cleaned_hashtag
    FROM STRING_SPLIT(fct.hashtags, ' ')
) AS ht
WHERE 
    dc.brand_name = 'Sony'
    AND ht.cleaned_hashtag <> ''
    AND ht.cleaned_hashtag NOT LIKE '% %'
    AND ht.cleaned_hashtag IS NOT NULL
GROUP BY 
    dc.brand_name, 
    ht.cleaned_hashtag
HAVING 
    ht.cleaned_hashtag <> ''