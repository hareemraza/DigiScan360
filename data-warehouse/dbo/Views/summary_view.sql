CREATE VIEW [dbo].[summary_view] AS (SELECT
    st.*,
    sp.title
FROM
    summaries_with_topics st
JOIN
    sony_productsall sp
ON
    st.ProductID = sp.ProductID
WHERE st.SellerID = 'sony'

)