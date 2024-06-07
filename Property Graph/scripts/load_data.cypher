// Load and create Seller nodes
LOAD CSV FROM 'file:///products.csv' AS line FIELDTERMINATOR '|'
WITH line SKIP 1
WHERE trim(line[14]) IS NOT NULL AND trim(line[14]) <> ''
MERGE (s:Seller {SellerID: trim(line[14])});


// Load and create Product nodes
LOAD CSV FROM 'file:///products.csv' AS line FIELDTERMINATOR '|'
WITH line SKIP 1
MERGE (p:Product {
    NumReviews: toInteger(coalesce(trim(line[2]), '0')),  
    Price: trim(line[3]), 
    Rating: toInteger(coalesce(trim(line[7]), '-1')),  
    Title: trim(line[8]),  
    Rating1: toInteger(coalesce(trim(line[9]), '-1')), 
    Rating2: toInteger(coalesce(trim(line[10]), '-1')),  
    Rating3: toInteger(coalesce(trim(line[11]), '-1')),  
    Rating4: toInteger(coalesce(trim(line[12]), '-1')),  
    Rating5: toInteger(coalesce(trim(line[13]), '-1')),  
    ProductID: trim(line[15])
});


// Create SELL relationship between Seller and Product nodes
LOAD CSV FROM 'file:///products.csv' AS line FIELDTERMINATOR '|'
WITH line SKIP 1
WHERE trim(line[14]) IS NOT NULL AND trim(line[14]) <> '' AND trim(line[15]) IS NOT NULL AND trim(line[15]) <> ''
MATCH (s:Seller {SellerID: trim(line[14])})
MATCH (p:Product {ProductID: trim(line[15])})
MERGE (s)-[:SELLS]->(p);


// Load and create Review nodes
LOAD CSV FROM 'file:///reviews.csv' AS line FIELDTERMINATOR '|'
WITH line SKIP 1
WHERE size(line) > 8 AND trim(line[0]) IS NOT NULL
MERGE (r:Review {
    ID: toInteger(trim(line[0]))
})
SET
    r.ReviewID = coalesce(trim(line[1]), 'None'),
    r.Title = trim(line[3]),
    r.Date = trim(line[7]);


// Load and create Feature nodes
LOAD CSV FROM 'file:///product_features.csv' AS line FIELDTERMINATOR '|'
WITH line SKIP 1
WHERE trim(line[1]) IS NOT NULL AND trim(line[1]) <> ''
MERGE (f:Feature {FeatureName: trim(line[1])});


// Create HAS_FEATURE relationship between Product and Feature nodes
LOAD CSV FROM 'file:///product_features.csv' AS line FIELDTERMINATOR '|'
WITH line SKIP 1
MATCH (p:Product {ProductID: trim(line[0])})  
MATCH (f:Feature {FeatureName: trim(line[1])})
WHERE trim(line[1]) IS NOT NULL AND trim(line[1]) <> '' AND trim(line[2]) IS NOT NULL
MERGE (p)-[:HAS_FEATURE {FeatureValue: trim(line[2])}]->(f);


// Create HAS_REVIEW relationship between Product and Review nodes
LOAD CSV FROM 'file:///reviews.csv' AS line FIELDTERMINATOR '|'
WITH line SKIP 1
WHERE trim(line[6]) IS NOT NULL AND trim(line[6]) <> '' AND trim(line[0]) IS NOT NULL
MATCH (p:Product {ProductID: trim(line[6])})
MATCH (r:Review {ID: toInteger(trim(line[0]))})
MERGE (p)-[rel:HAS_REVIEW]->(r)
SET
    rel.Rating = toInteger(coalesce(trim(line[2]), '-1')),
    rel.NumHelpful = toInteger(coalesce(trim(line[5]), '0')),
    rel.Sentiment = CASE trim(line[8]) WHEN 'True' THEN 1 ELSE 0 END;


// Create TALKS_ABOUT relationship between Review and Feature nodes
LOAD CSV FROM 'file:///review_features.csv' AS line FIELDTERMINATOR '|'
WITH line SKIP 1
WHERE trim(line[0]) IS NOT NULL AND trim(line[0]) <> '' AND trim(line[1]) IS NOT NULL AND trim(line[1]) <> ''
MATCH (r:Review {ID: toInteger(trim(line[0]))})
MATCH (f:Feature {FeatureName: trim(line[1])})
MERGE (r)-[:TALKS_ABOUT {Sentiment: CASE trim(line[2]) WHEN 'True' THEN 1 ELSE 0 END}]->(f);


// Load and create Theme nodes
LOAD CSV FROM 'file:///topics_by_brand.csv' AS line FIELDTERMINATOR '|'
WITH line SKIP 1
WHERE trim(line[2]) IS NOT NULL AND trim(line[2]) <> '' AND trim(line[1]) IS NOT NULL AND trim(line[1]) <> ''
MERGE (t:Theme {TopicName: trim(line[2]), Sentiment: trim(line[1])});


// Create DISCUSSES relationship between Review and Theme nodes
LOAD CSV FROM 'file:///summaries_with_topics.csv' AS line FIELDTERMINATOR '|'
WITH line SKIP 1
WHERE trim(line[0]) IS NOT NULL AND trim(line[0]) <> '' AND trim(line[4]) IS NOT NULL AND trim(line[4]) <> ''
MATCH (r:Review {ID: toInteger(trim(line[0]))})
MATCH (t:Theme {TopicName: trim(line[4]), Sentiment: trim(line[2])})
MERGE (r)-[:DISCUSSES {Value: coalesce(trim(line[3]), 'No Summary')}]->(t);


// Create HAS_FEEDBACKON relationship between Seller and Theme nodes
LOAD CSV FROM 'file:///topics_by_brand.csv' AS line FIELDTERMINATOR '|'
WITH line SKIP 1
WHERE trim(line[0]) IS NOT NULL AND trim(line[0]) <> '' AND trim(line[2]) IS NOT NULL AND trim(line[2]) <> ''
MATCH (s:Seller {SellerID: trim(line[0])})
MATCH (t:Theme {TopicName: trim(line[2]), Sentiment: trim(line[1])})
MERGE (s)-[:HAS_FEEDBACKON {Value: coalesce(trim(line[3]), 'No Summary')}]->(t);


