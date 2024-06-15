CREATE VIEW [dbo].[reviewSummaryTopicView] AS (SELECT 
    review_fk, 
    ProductID, 
    summary, 
    topic, 
    SellerID,
    sentiment,
    CASE 
        WHEN sentiment = 1 THEN 'Strength'
        ELSE 'Weakness'
    END AS sentiment_description
FROM reviewSummaryTopic
)