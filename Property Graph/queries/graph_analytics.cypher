// Query 1: Identify products with similar features for a brand
MATCH (s:Seller {SellerID: 'sony'})-[:SELLS]->(p1:Product)-[:HAS_FEATURE]->(f:Feature)<-[:HAS_FEATURE]-(p2:Product)<-[:SELLS]-(s2:Seller)
WHERE p1 <> p2 AND s <> s2
WITH p1, p2, s2, COUNT(f) AS sharedFeatures
WHERE sharedFeatures > 1
RETURN p1.Title AS Product1, p1.Rating AS Rating1, p2.Title AS Product2,s2.SellerID AS Seller2, p2.Rating AS Rating2, sharedFeatures
ORDER BY sharedFeatures DESC
LIMIT 10;



// Query 2: Find feature correlation with product ratings
MATCH (p:Product)-[:HAS_FEATURE]->(f:Feature)
WITH f.FeatureName AS Feature, COLLECT(p.Rating) AS Ratings
RETURN Feature, REDUCE(s = 0, x IN Ratings | s + x) / TOFLOAT(SIZE(Ratings)) AS AverageRating, SIZE(Ratings) AS ProductCount
ORDER BY AverageRating DESC;



//Query 3: Analyse the top features of the highest-rated products
MATCH (p:Product)-[:HAS_FEATURE]->(f:Feature)
WITH p, AVG(p.Rating) AS AvgRating
ORDER BY AvgRating DESC
LIMIT 10
MATCH (p)-[:HAS_FEATURE]->(f:Feature)
RETURN f.FeatureName AS Feature, COUNT(*) AS FeatureCount
ORDER BY FeatureCount DESC



// Query 4: Identify products that have reviews with the highest average rating mentioning a specific feature
MATCH (p:Product)-[:HAS_FEATURE]->(f:Feature {FeatureName: 'Battery Life'})
MATCH (r:Review)-[:TALKS_ABOUT]->(f)
WITH p, AVG(r.Rating) AS AvgReviewRating
RETURN p.Title AS ProductTitle, ROUND(AvgReviewRating,2) as AverageRating
ORDER BY AvgReviewRating DESC
LIMIT 10;



// Query 5: Lists all the features in all the products that have received reviews with positive sentiment, ordered in descending order based on the average rating
MATCH (p:Product)-[:HAS_FEATURE]->(f:Feature)
MATCH (p)-[rel:HAS_REVIEW]->(r:Review)
WHERE rel.Sentiment = 1
WITH f.FeatureName AS FeatureName, AVG(r.Rating) AS AvgReviewRating
RETURN FeatureName, AvgReviewRating
ORDER BY AvgReviewRating DESC;



// Query 6: Lists products with features that have received the highest average ratings where the sentiment is positive
MATCH (p:Product)-[:HAS_FEATURE]->(f:Feature)<-[:TALKS_ABOUT]-(r:Review)
MATCH (p)-[rel:HAS_REVIEW]->(r)
WHERE rel.Sentiment = 1
WITH p, f, AVG(r.Rating) AS AvgFeatureRating
RETURN p.Title AS ProductTitle, f.FeatureName AS FeatureName, AvgFeatureRating
ORDER BY AvgFeatureRating DESC
LIMIT 10;



// Query 7: Correlation Between Feature Sentiment, Review Rating, and Overall Product Rating
// Match products and their features
MATCH (p:Product)-[:HAS_FEATURE]->(f:Feature)
// Match reviews that talk about these features
MATCH (r:Review)-[:TALKS_ABOUT]->(f)
// Calculate the average rating for reviews mentioning the feature
MATCH (p)-[rel:HAS_REVIEW]->(r)
WITH p, f, AVG(r.Rating) AS AvgFeatureReviewRating,
     SUM(CASE WHEN rel.Sentiment = 1 THEN 1 ELSE 0 END) AS PositiveSentimentCount,
     SUM(CASE WHEN rel.Sentiment = 0 THEN 1 ELSE 0 END) AS NegativeSentimentCount,
     COUNT(r) AS TotalReviews
// Calculate the overall product rating
WITH p, f, AvgFeatureReviewRating, PositiveSentimentCount, NegativeSentimentCount, TotalReviews,
     AVG(p.Rating) AS OverallProductRating
RETURN p.Title AS ProductTitle,
       f.FeatureName AS FeatureName,
       AvgFeatureReviewRating,
       OverallProductRating,
       PositiveSentimentCount,
       NegativeSentimentCount,
       TotalReviews
ORDER BY OverallProductRating DESC, AvgFeatureReviewRating DESC;



// Query 8: Tracking Sentiment and Helpfulness Over Time for Specific Features
// Match features and the reviews that mention them
MATCH (p:Product)-[rel:HAS_REVIEW]->(r:Review)-[:TALKS_ABOUT]->(f:Feature)
WITH f, r, rel, date(r.Date) AS reviewDate
// Aggregate sentiment and helpfulness data over time
WITH f.FeatureName AS FeatureName,
     reviewDate,
     AVG(r.Rating) AS AvgFeatureReviewRating,
     SUM(CASE WHEN rel.Sentiment = 1 THEN 1 ELSE 0 END) AS PositiveSentimentCount,
     SUM(CASE WHEN rel.Sentiment = 0 THEN 1 ELSE 0 END) AS NegativeSentimentCount,
     SUM(rel.NumHelpful) AS TotalHelpfulCount,
     COUNT(r) AS TotalReviews
// Return aggregated data for each feature by date
RETURN FeatureName,
       reviewDate,
       AvgFeatureReviewRating,
       PositiveSentimentCount,
       NegativeSentimentCount,
       TotalHelpfulCount,
       TotalReviews
ORDER BY FeatureName, reviewDate;
