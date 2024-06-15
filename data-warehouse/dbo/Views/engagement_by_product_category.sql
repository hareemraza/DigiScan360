CREATE VIEW engagement_by_product_category AS
SELECT 
    CASE 
        WHEN hashtags LIKE '%#headphones%' OR hashtags LIKE '%#Earbuds%' OR hashtags LIKE '%#OverEar%' OR hashtags LIKE '%#OnEar%' OR hashtags LIKE '%#NoiseCancelling%' OR hashtags LIKE '%#TrueWireless%' THEN 'Headphones'
        WHEN hashtags LIKE '%#audio%' OR hashtags LIKE '%#soundquality%' OR hashtags LIKE '%#HiFi%' OR hashtags LIKE '%#BassHeads%' OR hashtags LIKE '%#MusicLover%' OR hashtags LIKE '%#PodcastLover%' THEN 'Audio'
        WHEN hashtags LIKE '%#tech%' OR hashtags LIKE '%#gadgets%' OR hashtags LIKE '%#TechInnovations%' OR hashtags LIKE '%#SmartTech%' OR hashtags LIKE '%#EcoFriendlyTech%' THEN 'Tech'
        WHEN hashtags LIKE '%#gaming%' OR hashtags LIKE '%#GamingGear%' OR hashtags LIKE '%#VirtualReality%' THEN 'Gaming'
        WHEN hashtags LIKE '%#lifestyle%' OR hashtags LIKE '%#TravelEssentials%' OR hashtags LIKE '%#FashionTech%' THEN 'Lifestyle'
        WHEN hashtags LIKE '%#MusicProduction%' OR hashtags LIKE '%#DJLife%' OR hashtags LIKE '%#StudioQuality%' OR hashtags LIKE '%#Instrumental%' THEN 'Music Production'
        ELSE 'Miscellaneous'
    END AS product_category,
    COUNT(tweet_id) AS total_tweets,
    SUM(like_count) AS total_likes,
    SUM(reply_count) AS total_replies,
    SUM(repost_count) AS total_reposts,
    SUM(quote_count) AS total_quotes,
    (SUM(like_count) + SUM(reply_count) + SUM(repost_count) + SUM(quote_count)) * 1.0 / COUNT(tweet_id) AS engagement_rate
FROM 
    fact_consumer_tweet
GROUP BY 
    CASE 
        WHEN hashtags LIKE '%#headphones%' OR hashtags LIKE '%#Earbuds%' OR hashtags LIKE '%#OverEar%' OR hashtags LIKE '%#OnEar%' OR hashtags LIKE '%#NoiseCancelling%' OR hashtags LIKE '%#TrueWireless%' THEN 'Headphones'
        WHEN hashtags LIKE '%#audio%' OR hashtags LIKE '%#soundquality%' OR hashtags LIKE '%#HiFi%' OR hashtags LIKE '%#BassHeads%' OR hashtags LIKE '%#MusicLover%' OR hashtags LIKE '%#PodcastLover%' THEN 'Audio'
        WHEN hashtags LIKE '%#tech%' OR hashtags LIKE '%#gadgets%' OR hashtags LIKE '%#TechInnovations%' OR hashtags LIKE '%#SmartTech%' OR hashtags LIKE '%#EcoFriendlyTech%' THEN 'Tech'
        WHEN hashtags LIKE '%#gaming%' OR hashtags LIKE '%#GamingGear%' OR hashtags LIKE '%#VirtualReality%' THEN 'Gaming'
        WHEN hashtags LIKE '%#lifestyle%' OR hashtags LIKE '%#TravelEssentials%' OR hashtags LIKE '%#FashionTech%' THEN 'Lifestyle'
        WHEN hashtags LIKE '%#MusicProduction%' OR hashtags LIKE '%#DJLife%' OR hashtags LIKE '%#StudioQuality%' OR hashtags LIKE '%#Instrumental%' THEN 'Music Production'
        ELSE 'Miscellaneous'
    END;