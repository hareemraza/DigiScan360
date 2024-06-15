CREATE PROCEDURE UpdateWarehouseSchema
AS
BEGIN
    IF OBJECT_ID('dbo.fact_consumer_tweet', 'U') IS NOT NULL
    BEGIN
        IF EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'fk_fact_consumer_tweet_tweet_date') AND parent_object_id = OBJECT_ID(N'fact_consumer_tweet'))
            ALTER TABLE fact_consumer_tweet DROP CONSTRAINT fk_fact_consumer_tweet_tweet_date;
    END

    IF OBJECT_ID('dbo.fact_facebook', 'U') IS NOT NULL
    BEGIN
        IF EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'fk_fact_facebook_created_date') AND parent_object_id = OBJECT_ID(N'fact_facebook'))
            ALTER TABLE fact_facebook DROP CONSTRAINT fk_fact_facebook_created_date;
    END

    IF OBJECT_ID('dbo.fact_user_tweet', 'U') IS NOT NULL
    BEGIN
        IF EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'fk_fact_user_tweet_record_date') AND parent_object_id = OBJECT_ID(N'fact_user_tweet'))
            ALTER TABLE fact_user_tweet DROP CONSTRAINT fk_fact_user_tweet_record_date;
    END

    IF OBJECT_ID('dbo.fact_reviews', 'U') IS NOT NULL
    BEGIN
        IF EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'fk_fact_reviews_ProductID') AND parent_object_id = OBJECT_ID(N'fact_reviews'))
            ALTER TABLE fact_reviews DROP CONSTRAINT fk_fact_reviews_ProductID;

        IF EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'fk_fact_reviews_date') AND parent_object_id = OBJECT_ID(N'fact_reviews'))
            ALTER TABLE fact_reviews DROP CONSTRAINT fk_fact_reviews_date;
    END

    IF OBJECT_ID('dbo.fact_products', 'U') IS NOT NULL
    BEGIN
        IF EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'fk_fact_products_ProductID') AND parent_object_id = OBJECT_ID(N'fact_products'))
            ALTER TABLE fact_products DROP CONSTRAINT fk_fact_products_ProductID;

        IF EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'fk_fact_products_date_accessed') AND parent_object_id = OBJECT_ID(N'fact_products'))
            ALTER TABLE fact_products DROP CONSTRAINT fk_fact_products_date_accessed;
    END

    -- Drop primary key constraints if they exist
    IF OBJECT_ID('dbo.dim_products', 'U') IS NOT NULL
    BEGIN
        IF EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'dim_products') AND name = N'pk_dim_products_ProductID')
            ALTER TABLE dim_products DROP CONSTRAINT pk_dim_products_ProductID;
    END

    IF OBJECT_ID('dbo.fact_products', 'U') IS NOT NULL
    BEGIN
        IF EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'fact_products') AND name = N'pk_fact_products')
            ALTER TABLE fact_products DROP CONSTRAINT pk_fact_products;
    END

    IF OBJECT_ID('dbo.dim_time', 'U') IS NOT NULL
    BEGIN
        IF EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'dim_time') AND name = N'pk_dim_time_date')
            ALTER TABLE dim_time DROP CONSTRAINT pk_dim_time_date;
    END

    -- Step 1: Create a new dim_products table with the correct schema
    DROP TABLE IF EXISTS new_dim_products;
    CREATE TABLE new_dim_products (
        ProductID VARCHAR(8000) NOT NULL,
        title VARCHAR(8000) NOT NULL,
        img_url VARCHAR(8000),
        product_url VARCHAR(8000),
        SellerID VARCHAR(8000)
    );

    -- Insert data from the existing dim_products table into the new table
    INSERT INTO new_dim_products (ProductID, title, img_url, product_url, SellerID)
    SELECT ProductID, title, img_url, product_url, SellerID
    FROM dim_products;

    -- Drop the existing dim_products table
    DROP TABLE IF EXISTS dim_products;

    -- Rename the new_dim_products table to dim_products
    EXEC sp_rename 'new_dim_products', 'dim_products';

    DROP TABLE IF EXISTS seller;
    CREATE TABLE seller (SellerID VARCHAR(8000) NOT NULL)
    ALTER TABLE seller
    ADD CONSTRAINT pk_seller_sellerid PRIMARY KEY NONCLUSTERED (SellerID) NOT ENFORCED;
    INSERT INTO seller (SellerID)
    SELECT DISTINCT SellerID FROM dim_products WHERE SellerID IS NOT NULL;

    -- Step 2: Create a new fact_products table with the correct schema
    DROP TABLE IF EXISTS new_fact_products;
    CREATE TABLE new_fact_products (
        ProductID VARCHAR(8000) NOT NULL,
        date_accessed DATE NOT NULL,
        num_reviews INT,
        rating FLOAT,
        rating_1 INT,
        rating_2 INT,
        rating_3 INT,
        rating_4 INT,
        rating_5 INT,
        price FLOAT
    );

    -- Insert data from the existing fact_products table into the new table
    INSERT INTO new_fact_products (ProductID, date_accessed, num_reviews, rating, rating_1, rating_2, rating_3, rating_4, rating_5, price)
    SELECT ProductID, date_accessed, num_reviews, rating, rating_1, rating_2, rating_3, rating_4, rating_5, price
    FROM fact_products;

    -- Drop the existing fact_products table
    DROP TABLE IF EXISTS fact_products;

    -- Rename the new_fact_products table to fact_products
    EXEC sp_rename 'new_fact_products', 'fact_products';

    -- Step 3: Create a new fact_reviews table with the correct schema
    DROP TABLE IF EXISTS new_fact_reviews;
    CREATE TABLE new_fact_reviews (
        ProductID VARCHAR(8000) NOT NULL,
        date DATE,
        rating INT,
        num_helpful INT, 
        sentiment BIT,
        id INT NOT NULL,
        review_id VARCHAR(8000)
    );

    -- Insert data from the existing fact_reviews table into the new table
    INSERT INTO new_fact_reviews (id, review_id, ProductID, date, rating, num_helpful, sentiment)
    SELECT id, review_id, ProductID, date, rating, num_helpful, sentiment
    FROM fact_reviews;

    -- Drop the existing fact_reviews table
    DROP TABLE IF EXISTS fact_reviews;

    -- Rename the new_fact_reviews table to fact_reviews
    EXEC sp_rename 'new_fact_reviews', 'fact_reviews';

    -- Step 4: Create a new dim_time table with the correct schema
    DROP TABLE IF EXISTS new_dim_time;
    CREATE TABLE new_dim_time (
        date DATE NOT NULL,
        day INT,
        month INT,
        year INT,
        quarter INT
    );

    -- Insert data from the existing dim_time table into the new table
    INSERT INTO new_dim_time (date, day, month, year, quarter)
    SELECT date, day, month, year, quarter
    FROM dim_time;

    -- Drop the existing dim_time table
    DROP TABLE IF EXISTS dim_time;

    -- Rename the new_dim_time table to dim_time
    EXEC sp_rename 'new_dim_time', 'dim_time';

    DROP TABLE IF EXISTS  new_reviewSummaryTopic;
    CREATE TABLE new_reviewSummaryTopic (
        review_fk int NOT NULL,
        ProductID VARCHAR(8000) NOT NULL,
        sentiment BIT,
        summary VARCHAR(8000),
        topic VARCHAR(8000),
        SellerID VARCHAR(8000)
    );

    -- Insert data from the existing summaries_with_topic table into the new table
    INSERT INTO new_reviewSummaryTopic (review_fk, ProductID, sentiment, summary, topic, SellerID)
    SELECT review_fk, ProductID, sentiment, summary, topic, SellerID
    FROM reviewSummaryTopic;

    -- Drop the existing summaries_with_topic table
    DROP TABLE IF EXISTS reviewSummaryTopic;

    -- Rename the new_dim_products table to dim_products
    EXEC sp_rename 'new_reviewSummaryTopic', 'reviewSummaryTopic';
END;